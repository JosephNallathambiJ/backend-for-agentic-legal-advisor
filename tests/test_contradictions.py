"""
tests/test_contradictions.py - Contradiction Detection Tests
Verifies cross-document conflicts (dates, amounts) are surfaced and disclosed, never reconciled silently.
"""

import pytest
from core.provenance import EvidenceLedger
from core.contradiction_detector import ContradictionDetector

def test_detect_conflicting_arrest_dates():
    ledger = EvidenceLedger()
    detector = ContradictionDetector(ledger)
    
    # Doc 1
    ledger.add_fact(
        text="The accused was arrested on 12 June 2024 at his residence.",
        document_id="police_remand.pdf",
        date_referenced="12 June 2024"
    )
    
    # Doc 2
    ledger.add_fact(
        text="The accused was arrested on 14 June 2024 at the railway station.",
        document_id="case_diary.pdf",
        date_referenced="14 June 2024"
    )
    
    conflicts = detector.detect_contradictions()
    assert len(conflicts) >= 1
    c = conflicts[0]
    assert c.contradiction_type == "date_mismatch"
    assert "12 June 2024" in c.statement_a or "12 June 2024" in c.statement_b
    assert "14 June 2024" in c.statement_a or "14 June 2024" in c.statement_b
    assert c.resolution_policy == "DISCLOSE_CONFLICT_DO_NOT_RESOLVE"

def test_detect_conflicting_claim_amounts():
    ledger = EvidenceLedger()
    detector = ContradictionDetector(ledger)
    
    ledger.add_fact(
        text="The complainant claims damages of Rs. 50,000.",
        document_id="complaint.txt"
    )
    ledger.add_fact(
        text="The bill documents outstanding dues of Rs. 1,50,000.",
        document_id="invoice.txt"
    )
    
    conflicts = detector.detect_contradictions()
    assert len(conflicts) >= 1
    assert any(c.contradiction_type == "amount_conflict" for c in conflicts)
