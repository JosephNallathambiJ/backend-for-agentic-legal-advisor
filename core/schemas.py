"""
core/schemas.py - Typed Pydantic data contracts
Defines Fact, Evidence, Claim, Verdict, Contradiction, PreDraftAudit, and Pipeline contracts.
"""

from typing import List, Dict, Optional, Any, Literal
from pydantic import BaseModel, Field
import time

class Fact(BaseModel):
    fact_id: str
    text: str
    document_id: str
    page: int = 1
    character_offset_start: int = 0
    character_offset_end: int = 0
    extraction_method: str = "regex_parser"
    entity: Optional[str] = None
    date_referenced: Optional[str] = None

class Evidence(BaseModel):
    evidence_id: str
    evidence_type: Literal["case_fact", "statute", "precedent", "user_assertion"]
    jurisdiction: str = "INDIA" # INDIA, US, UK, EU
    source_id: str
    source_title: str
    source_path: Optional[str] = None
    section: Optional[str] = None
    page: Optional[int] = None
    text_span: str
    locator: str # e.g. "Doc1:p1:char10-50" or "BNS_2023:Sec303"
    version: str = "official_snapshot"
    hash: str # cryptographic sha256
    retrieved_at: float = Field(default_factory=time.time)

class Claim(BaseModel):
    claim_id: str
    text: str
    claim_type: Literal["statutory", "factual", "procedural", "inference"]
    evidence_ids: List[str] = Field(default_factory=list)
    citation_ids: List[str] = Field(default_factory=list)
    risk_level: Literal["low", "medium", "high"] = "low"
    is_quote: bool = False
    quote_text: Optional[str] = None

class Verdict(BaseModel):
    claim_id: str
    status: Literal["PASS", "FLAG", "REJECT", "NOT_VERIFIED"]
    reason_codes: List[str] = Field(default_factory=list)
    checks: Dict[str, bool] = Field(default_factory=dict)
    reviewer_required: bool = False
    audit_notes: Optional[str] = None

class Contradiction(BaseModel):
    conflict_id: str
    topic: str
    statement_a: str
    evidence_id_a: str
    doc_a: str
    statement_b: str
    evidence_id_b: str
    doc_b: str
    contradiction_type: Literal["date_mismatch", "factual_conflict", "identity_mismatch", "amount_conflict"]
    resolution_policy: str = "DISCLOSE_CONFLICT_DO_NOT_RESOLVE"

class PreDraftAudit(BaseModel):
    known_facts: List[str] = Field(default_factory=list)
    unknown_facts: List[str] = Field(default_factory=list)
    conflicting_facts: List[Contradiction] = Field(default_factory=list)
    explicit_citations: List[str] = Field(default_factory=list)
    candidate_statutes: List[Dict[str, Any]] = Field(default_factory=list)
    unavailable_evidence: List[str] = Field(default_factory=list)
    questions_for_counsel: List[str] = Field(default_factory=list)
    drafting_risks: List[str] = Field(default_factory=list)

class StructuredDraft(BaseModel):
    task_type: str
    title: str
    claims: List[Claim] = Field(default_factory=list)
    missing_information: List[str] = Field(default_factory=list)
    uncertainties: List[str] = Field(default_factory=list)
    draft_text: str = ""
    verdicts: Dict[str, Verdict] = Field(default_factory=dict)

class TelemetryReport(BaseModel):
    cpu_percent: float = 0.0
    ram_used_mb: float = 0.0
    ram_limit_mb: float = 3584.0
    ram_budget_percent: float = 0.0
    retrieval_latency_ms: float = 0.0
    llm_latency_ms: float = 0.0
    verification_latency_ms: float = 0.0
    total_latency_ms: float = 0.0
    cache_hit_rate: float = 1.0
    outbound_network_calls: int = 0
    network_status: str = "DISABLED"

class PipelineResult(BaseModel):
    workflow: str
    query_or_task: str
    pre_draft_audit: PreDraftAudit
    structured_draft: StructuredDraft
    claims: List[Claim]
    verdicts: List[Verdict]
    evidence_records: List[Evidence]
    contradictions: List[Contradiction]
    telemetry: TelemetryReport
    final_audited_text: str
