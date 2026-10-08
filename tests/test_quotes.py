"""
tests/test_quotes.py - Exact Quotation Validation Tests
Verifies that quotes matching source text pass, while altered/fabricated quotes are REJECTED.
"""

import pytest
from core.provenance import EvidenceLedger
from core.local_legal_retriever import LocalLegalRetriever
from core.verifier import DeterministicVerifier
from core.schemas import Claim

def test_verbatim_quote_passes():
    ledger = EvidenceLedger()
    retriever = LocalLegalRetriever(ledger)
    verifier = DeterministicVerifier(ledger)
    
    ev = retriever.lookup_section("BNS_2023", "303")
    assert ev is not None
    
    # Exact snippet from Section 303
    quote_snippet = "Whoever, intending to take dishonestly any movable property"
    claim = Claim(
        claim_id="C010",
        text=f'The statute states: "{quote_snippet}" out of possession.',
        claim_type="statutory",
        evidence_ids=[ev.evidence_id],
        citation_ids=[ev.locator],
        is_quote=True,
        quote_text=quote_snippet
    )
    
    verdict = verifier.verify_claim(claim)
    assert verdict.checks["quotes_authentic"] is True
    assert verdict.status == "PASS"

def test_altered_quote_rejected():
    ledger = EvidenceLedger()
    retriever = LocalLegalRetriever(ledger)
    verifier = DeterministicVerifier(ledger)
    
    ev = retriever.lookup_section("BNS_2023", "303")
    assert ev is not None
    
    # Altered text placed in quotes
    altered_quote = "Whoever takes any gold ornaments with malice aforethought"
    claim = Claim(
        claim_id="C011",
        text=f'Section 303 explicitly states: "{altered_quote}" shall be hanged.',
        claim_type="statutory",
        evidence_ids=[ev.evidence_id],
        citation_ids=[ev.locator],
        is_quote=True,
        quote_text=altered_quote
    )
    
    verdict = verifier.verify_claim(claim)
    assert verdict.status == "REJECT"
    assert any("ERR_ALTERED_OR_FABRICATED_QUOTE" in r for r in verdict.reason_codes)
