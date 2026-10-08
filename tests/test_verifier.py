"""
tests/test_verifier.py - Deterministic Verifier Gates & Fail-Closed Tests
Covers Checks A through H and fail-closed security invariants.
"""

import pytest
from core.provenance import EvidenceLedger
from core.local_legal_retriever import LocalLegalRetriever
from core.verifier import DeterministicVerifier
from core.schemas import Claim

def test_fact_source_mismatch_rejected():
    """Case specific facts must cite case evidence, not statutes."""
    ledger = EvidenceLedger()
    retriever = LocalLegalRetriever(ledger)
    verifier = DeterministicVerifier(ledger)
    
    # Retrieve a statute
    ev_statute = retriever.lookup_section("BNS_2023", "303")
    
    # Asserting that the accused committed a theft on a specific date, citing ONLY the statute
    claim = Claim(
        claim_id="C020",
        text="The accused Ramesh Kumar stole the diamond necklace on 15 August 2024.",
        claim_type="factual",
        evidence_ids=[ev_statute.evidence_id], # Statute cannot substantiate case occurrence!
        citation_ids=[ev_statute.locator]
    )
    
    verdict = verifier.verify_claim(claim)
    assert verdict.status == "REJECT"
    assert any("ERR_FACT_SOURCE_MISMATCH" in r for r in verdict.reason_codes)

def test_case_fact_with_case_evidence_passes():
    """Proper case fact citing uploaded case dossier passes."""
    ledger = EvidenceLedger()
    verifier = DeterministicVerifier(ledger)
    
    fact = ledger.add_fact(
        text="Ramesh Kumar was arrested on 15 August 2024 from M.G. Road.",
        document_id="fir_copy.pdf",
        page=1,
        offset_start=0,
        offset_end=58
    )
    # The corresponding evidence was registered
    ev_id = ledger.list_evidence()[0].evidence_id
    
    claim = Claim(
        claim_id="C021",
        text="Ramesh Kumar was arrested on 15 August 2024 from M.G. Road.",
        claim_type="factual",
        evidence_ids=[ev_id]
    )
    
    verdict = verifier.verify_claim(claim)
    assert verdict.status == "PASS"

def test_semantic_contradiction_rejected():
    """NLI contradiction check rejects opposing assertions."""
    ledger = EvidenceLedger()
    verifier = DeterministicVerifier(ledger)
    
    fact = ledger.add_fact(
        text="The applicant was never present at the scene of the occurrence.",
        document_id="alibi_affidavit.txt"
    )
    ev_id = ledger.list_evidence()[0].evidence_id
    
    # Opposite assertion
    claim = Claim(
        claim_id="C022",
        text="The applicant was present at the scene of the occurrence.",
        claim_type="factual",
        evidence_ids=[ev_id]
    )
    
    verdict = verifier.verify_claim(claim)
    assert verdict.status == "REJECT"
    assert any("CONTRADICTION" in r for r in verdict.reason_codes)

def test_fail_closed_on_missing_evidence():
    ledger = EvidenceLedger()
    verifier = DeterministicVerifier(ledger)
    
    claim = Claim(
        claim_id="C023",
        text="Valid proposition with missing evidence link.",
        claim_type="statutory",
        evidence_ids=[]
    )
    
    verdict = verifier.verify_claim(claim)
    assert verdict.status == "REJECT"
    assert "ERR_NO_EVIDENCE_MAPPED" in verdict.reason_codes
