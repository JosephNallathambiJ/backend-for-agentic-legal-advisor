"""
tests/test_citations.py - Citation Allowlist & Integrity Verification Tests
Ensures fabricated, altered, or unverified legal citations are strictly REJECTED.
"""

import pytest
from core.provenance import EvidenceLedger
from core.local_legal_retriever import LocalLegalRetriever
from core.verifier import DeterministicVerifier
from core.schemas import Claim

def test_authentic_citation_passes():
    ledger = EvidenceLedger()
    retriever = LocalLegalRetriever(ledger)
    verifier = DeterministicVerifier(ledger)
    
    # Retrieve authentic statute
    ev = retriever.lookup_section("BNS_2023", "303")
    assert ev is not None
    
    claim = Claim(
        claim_id="C001",
        text=f"Section 303 of BNS defines theft as dishonestly moving movable property without consent.",
        claim_type="statutory",
        evidence_ids=[ev.evidence_id],
        citation_ids=[ev.locator]
    )
    
    verdict = verifier.verify_claim(claim)
    assert verdict.status == "PASS"
    assert verdict.checks["citations_allowed"] is True

def test_fabricated_citation_rejected():
    ledger = EvidenceLedger()
    verifier = DeterministicVerifier(ledger)
    
    # Claim cites fabricated Section 999 of BNS
    claim = Claim(
        claim_id="C002",
        text="Section 999 BNS provides for capital punishment for civil contempt.",
        claim_type="statutory",
        evidence_ids=[],
        citation_ids=["BNS_2023:Sec999"]
    )
    
    verdict = verifier.verify_claim(claim)
    assert verdict.status == "REJECT"
    assert any("ERR_NO_EVIDENCE_MAPPED" in r or "ERR_CITATION_NOT_IN_LOCAL_CORPUS" in r for r in verdict.reason_codes)

def test_unresolved_citation_id_rejected():
    ledger = EvidenceLedger()
    retriever = LocalLegalRetriever(ledger)
    verifier = DeterministicVerifier(ledger)
    
    ev = retriever.lookup_section("BNS_2023", "303")
    
    # Claim links to a fake evidence ID not present in the ledger
    claim = Claim(
        claim_id="C003",
        text="Section 303 BNS applies.",
        claim_type="statutory",
        evidence_ids=["E_NONEXISTENT_9999"],
        citation_ids=["BNS_2023:Sec303"]
    )
    
    verdict = verifier.verify_claim(claim)
    assert verdict.status == "REJECT"
    assert any("ERR_EVIDENCE_NOT_FOUND" in r for r in verdict.reason_codes)
