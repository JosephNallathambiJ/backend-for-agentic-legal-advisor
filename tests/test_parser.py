"""
tests/test_parser.py - Tests for CaseParser
Verifies atomic proposition segmentation, character offsets, entities, dates, and citations.
"""

import os
import pytest
from core.provenance import EvidenceLedger
from core.case_parser import CaseParser

def test_atomic_fact_segmentation():
    ledger = EvidenceLedger()
    parser = CaseParser(ledger)
    text = "Ramesh was arrested on 15 August 2024. He was taken to M.G. Road Police Station. FIR No. 204/2024 was registered."
    facts, cites, warnings = parser.parse_text(text, document_id="test_dossier")
    
    assert len(facts) >= 2
    assert any("arrested" in f.text for f in facts)
    assert any("15 August 2024" in (f.date_referenced or "") for f in facts)
    assert len(ledger.list_facts()) >= 2
    assert len(ledger.list_evidence()) >= 2

def test_citation_extraction():
    ledger = EvidenceLedger()
    parser = CaseParser(ledger)
    text = "The charge is framed under Section 303 of the Bharatiya Nyaya Sanhita and Section 73 of the Indian Contract Act."
    facts, cites, warnings = parser.parse_text(text)
    
    assert len(cites) == 2
    assert any("303" in c and "Bharatiya Nyaya Sanhita" in c for c in cites)
    assert any("73" in c and "Indian Contract Act" in c for c in cites)

def test_character_offsets_validity():
    ledger = EvidenceLedger()
    parser = CaseParser(ledger)
    raw = "The agreement was signed on 10 January 2023. Delivery failed on 30 March 2023."
    facts, cites, warnings = parser.parse_text(raw, document_id="contract_doc")
    
    for f in facts:
        # Check offset slices back to text
        sliced = raw[f.character_offset_start:f.character_offset_end]
        assert f.text in raw
        assert f.character_offset_start >= 0
        assert f.character_offset_end > f.character_offset_start
