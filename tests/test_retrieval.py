"""
tests/test_retrieval.py - Tests for Local Legal Corpus Retrieval
Verifies offline SQLite lookup, hash calculation, and zero-fabrication fallback.
"""

import pytest
from core.provenance import EvidenceLedger
from core.local_legal_retriever import LocalLegalRetriever
from core.legal_router import LegalRouter

def test_lookup_authentic_statutes():
    ledger = EvidenceLedger()
    retriever = LocalLegalRetriever(ledger)
    
    # BNS 303 (Theft)
    ev_bns = retriever.lookup_section("BNS_2023", "303")
    assert ev_bns is not None
    assert ev_bns.evidence_type == "statute"
    assert "theft" in ev_bns.text_span.lower()
    assert ev_bns.hash != ""
    assert ev_bns.locator == "BNS_2023:Sec303"
    
    # ICA 73 (Breach of contract damages)
    ev_ica = retriever.lookup_section("ICA_1872", "73")
    assert ev_ica is not None
    assert "compensation" in ev_ica.text_span.lower() or "breach" in ev_ica.text_span.lower()

def test_nonexistent_section_fails_closed():
    ledger = EvidenceLedger()
    retriever = LocalLegalRetriever(ledger)
    
    # Section 999 does not exist in BNS
    ev_fake = retriever.lookup_section("BNS_2023", "999")
    assert ev_fake is None
    
    # Fake act ID
    ev_fake_act = retriever.lookup_section("NON_EXISTENT_ACT_1999", "1")
    assert ev_fake_act is None

def test_legal_router_priority():
    router = LegalRouter()
    # Explicit citation in query
    cands = router.route_candidates("What are bail conditions under Section 303 BNS?")
    assert len(cands) > 0
    top = cands[0]
    assert top["act_id"] == "BNS_2023"
    assert top["target_section"] == "303"
    assert top["source_method"] == "explicit_citation"
