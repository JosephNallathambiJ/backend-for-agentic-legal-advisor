"""
api/app.py - Offline Backend REST API
Headless JSON service with multi-jurisdiction support (India, US, UK, EU).
Zero external network calls (NETWORK = DISABLED).
"""

import os
import sys
import json
import psutil
import pandas as pd
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if WORKSPACE_DIR not in sys.path:
    sys.path.insert(0, WORKSPACE_DIR)

from core.pipeline_coordinator import PipelineCoordinator
from core.schemas import PipelineResult, Claim, Verdict, Evidence
from core.provenance import EvidenceLedger
from core.local_legal_retriever import LocalLegalRetriever
from core.verifier import DeterministicVerifier

app = FastAPI(
    title="Legal Verification Assistant API",
    description="Deterministic Verification Architecture - Multi-Jurisdiction Local Backend",
    version="2.0.0"
)

# Localhost only CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

coordinator = PipelineCoordinator()

class RunRequest(BaseModel):
    workflow: str = Field(..., description="Workflow: bail_petition, contract_case_review, legal_research, rag_chat")
    query: str = Field(..., description="Legal query, issue description, or task")
    raw_text: Optional[str] = Field(None, description="Raw text of uploaded case dossier or contract")
    document_paths: Optional[List[str]] = Field(None, description="Local absolute paths to authorized dossier files")
    jurisdiction: Optional[str] = Field(None, description="Optional jurisdiction filter: INDIA, US, UK, EU")

class LookupRequest(BaseModel):
    act_id: str = Field(..., description="Canonical Act ID e.g. BNS_2023, US_TITLE_18, UK_THEFT_1968, EU_GDPR_2016")
    section_number: str = Field(..., description="Section or Article number e.g. 303, 641, 1, 5")

class VerifyRequest(BaseModel):
    claims: List[Claim] = Field(..., description="List of atomic claims to verify")

@app.get("/health")
async def health_check():
    """Returns local system health, memory status, and offline verification confirmation."""
    process = psutil.Process(os.getpid())
    mem_mb = process.memory_info().rss / (1024 * 1024)
    registry_file = os.path.join(WORKSPACE_DIR, "data", "registry", "registry_index.json")
    act_count = 0
    if os.path.exists(registry_file):
        with open(registry_file, "r", encoding="utf-8") as f:
            act_count = len(json.load(f))

    return {
        "status": "HEALTHY",
        "mode": "OFFLINE_LOCAL",
        "network": "DISABLED (0 Outbound Calls)",
        "resident_ram_mb": round(mem_mb, 1),
        "target_ram_budget_mb": 3584.0,
        "indexed_acts": act_count,
        "base_model": "Gemma 4 12B",
        "supported_jurisdictions": [
            "INDIA", "US", "UK", "EU",
            "BELARUS", "BULGARIA", "CZECH_REPUBLIC", "DENMARK",
            "ESTONIA", "FINLAND", "HUNGARY", "ICELAND", "IRELAND",
            "LATVIA", "LITHUANIA", "NORWAY", "POLAND", "ROMANIA",
            "RUSSIA", "SLOVAKIA", "SWEDEN", "UKRAINE"
        ]
    }

@app.get("/api/jurisdictions")
async def get_jurisdictions():
    """Returns available jurisdictions and statutory counts."""
    csv_dir = os.path.join(WORKSPACE_DIR, "data", "csv")
    res = {}
    csv_mappings = [
        ("INDIA", "india_central_acts.csv"),
        ("US", "us_federal_statutes.csv"),
        ("UK", "uk_statutes.csv"),
        ("EU", "eu_regulations.csv"),
        ("NORTHERN_EASTERN_EUROPE", "northern_eastern_europe_constitutions.csv")
    ]
    for jur, fname in csv_mappings:
        p = os.path.join(csv_dir, fname)
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                res[jur] = max(0, sum(1 for _ in f) - 1)
        else:
            res[jur] = 0
    return res

@app.get("/api/portals")
async def get_court_portals():
    """Returns official court and legislation portals across all supported countries."""
    portals_file = os.path.join(WORKSPACE_DIR, "data", "csv", "court_portals_registry.csv")
    if os.path.exists(portals_file):
        df = pd.read_csv(portals_file)
        return JSONResponse(content=df.to_dict(orient="records"))
    return []

@app.get("/api/official_link")
async def get_official_link(act_id: str, section: Optional[str] = None):
    """Resolves authoritative official portal URL for an act and section without external network calls."""
    from core.statute_web_linker import statute_linker
    return statute_linker.resolve_statute_link(act_id, section)

@app.post("/api/link_citations")
async def link_citations_in_text(payload: Dict[str, str]):
    """Extracts statutory citations from input text and resolves official government URLs."""
    from core.statute_web_linker import statute_linker
    text = payload.get("text", "")
    return statute_linker.link_citations_in_text(text)

@app.post("/api/run")
async def run_workflow(req: RunRequest):
    """Executes the full bounded agentic legal pipeline and returns typed result JSON."""
    try:
        coordinator.reset_session()
        result: PipelineResult = coordinator.orchestrator.execute_workflow(
            workflow=req.workflow,
            query=req.query,
            document_paths=req.document_paths,
            raw_text_dossier=req.raw_text
        )
        return JSONResponse(content=result.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"BACKEND_PIPELINE_ERROR: {str(e)}")

@app.get("/api/test_cases")
async def list_test_cases():
    """Returns benchmark dispute test cases."""
    test_cases_path = os.path.join(WORKSPACE_DIR, "data", "test_cases", "sample_disputes.json")
    if os.path.exists(test_cases_path):
        with open(test_cases_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

@app.post("/api/lookup")
async def lookup_statute(req: LookupRequest):
    """Direct offline lookup of authentic section from SQLite corpus cache."""
    ledger = EvidenceLedger()
    retriever = LocalLegalRetriever(ledger)
    ev = retriever.lookup_section(req.act_id, req.section_number)
    if not ev:
        raise HTTPException(
            status_code=404,
            detail=f"SECTION_NOT_FOUND: {req.act_id} Section {req.section_number} not in local corpus"
        )
    return JSONResponse(content=ev.model_dump())

@app.post("/api/verify")
async def verify_claims(req: VerifyRequest):
    """Standalone claim verification service against current evidence ledger."""
    try:
        verdicts = coordinator.orchestrator.verifier.verify_all(req.claims)
        return JSONResponse(content=[v.model_dump() for v in verdicts])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"VERIFICATION_ERROR: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
