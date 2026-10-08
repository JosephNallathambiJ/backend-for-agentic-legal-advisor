"""
tests/test_end_to_end.py - End-to-End Workflow & Integration Tests
Validates all 4 primary workflows:
  1. Contract / Case Review
  2. Legal Drafting
  3. Legal Research
  4. Grounded RAG Chat (including abstention)
"""

import pytest
from core.pipeline_coordinator import PipelineCoordinator

def test_workflow_contract_review():
    coordinator = PipelineCoordinator()
    contract_text = (
        "Service Level Agreement: Alpha Technologies agrees to deliver cloud services to Beta Retail. "
        "Delivery deadline is 15 October 2024. Penalty for delayed breach is Rs. 1,00,000 per week. "
        "Any disputes shall be resolved under the Indian Contract Act."
    )
    res = coordinator.run_contract_case_review(
        query="Review contract obligations and breach penalties",
        raw_text=contract_text
    )
    
    assert res.workflow == "contract_case_review"
    assert len(res.claims) > 0
    assert len(res.evidence_records) > 0
    assert res.telemetry.outbound_network_calls == 0
    assert res.telemetry.ram_used_mb <= 3584.0

def test_workflow_legal_drafting_bail():
    coordinator = PipelineCoordinator()
    case_facts = (
        "Accused Mohan was arrested on 10 July 2024 by City Police. "
        "The charge is theft under Section 303 of BNS 2023. "
        "Accused has clean antecedents and is a permanent resident."
    )
    res = coordinator.run_legal_drafting(
        draft_type="bail_petition",
        query="Draft regular bail petition under Section 303 BNS",
        raw_text=case_facts
    )
    
    assert res.workflow == "bail_petition"
    assert "APPLICATION FOR BAIL" in res.structured_draft.title
    assert "[COURT NAME NOT PROVIDED]" in res.final_audited_text
    assert any(c.claim_type == "statutory" for c in res.claims)
    assert any(c.claim_type == "factual" for c in res.claims)

def test_workflow_legal_research():
    coordinator = PipelineCoordinator()
    res = coordinator.run_legal_research(
        issue_query="What are the essential elements of breach damages under Section 73 of Indian Contract Act 1872?"
    )
    
    assert res.workflow == "legal_research"
    assert len(res.claims) > 0
    assert any("73" in ev.locator for ev in res.evidence_records)

def test_workflow_rag_chat_abstention():
    coordinator = PipelineCoordinator()
    # Query with no evidence in dossier or corpus
    res = coordinator.run_rag_chat(
        question="What were the secret internal code names used by company XYZ in 1999?"
    )
    
    assert res.workflow == "rag_chat"
    # Must abstain under verifiability over fluency rule
    assert "NOT_VERIFIED" in res.final_audited_text
