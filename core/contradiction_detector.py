"""
core/contradiction_detector.py - Contradiction and Conflict Detection Engine
Detects conflicting statements (e.g. conflicting arrest dates, differing financial amounts)
across uploaded case dossiers. Follows strict policy: Disclose conflict, never reconcile silently.
"""

import re
from typing import List, Dict, Tuple
from core.schemas import Contradiction, Fact, Evidence
from core.provenance import EvidenceLedger

# Date matching regex
DATE_EXTRACTION = re.compile(
    r"\b(\d{1,2}(?:st|nd|rd|th)?[\s\/\-\.](?:January|February|March|April|May|June|July|August|September|October|November|December|[0-9]{1,2})(?:[\s\/\-\.]\d{2,4})?)\b",
    re.IGNORECASE
)

# Currency / amount regex
AMOUNT_EXTRACTION = re.compile(
    r"(?:Rs\.?|INR|₹|\$|USD|£|GBP|€|EUR)\s*([\d,]+(?:\.\d{2})?)",
    re.IGNORECASE
)

class ContradictionDetector:
    def __init__(self, ledger: EvidenceLedger):
        self.ledger = ledger

    def detect_contradictions(self) -> List[Contradiction]:
        """
        Scans all facts and evidence in the ledger to surface contradictory assertions.
        """
        contradictions: List[Contradiction] = []
        facts = self.ledger.list_facts()
        conflict_idx = 1

        # 1. Date Contradictions on shared event topics (e.g. Arrest, Occurrence, Agreement)
        event_topics = ["arrest", "incident", "occurrence", "agreement", "termination", "payment"]
        for topic in event_topics:
            topic_facts = [f for f in facts if topic in f.text.lower()]
            if len(topic_facts) >= 2:
                # Compare pairs
                for i in range(len(topic_facts)):
                    for j in range(i + 1, len(topic_facts)):
                        f1 = topic_facts[i]
                        f2 = topic_facts[j]
                        
                        d1 = f1.date_referenced or self._find_date(f1.text)
                        d2 = f2.date_referenced or self._find_date(f2.text)
                        
                        if d1 and d2 and d1.lower() != d2.lower():
                            # Conflicting dates for the same event
                            ev1 = self._find_evidence_for_fact(f1)
                            ev2 = self._find_evidence_for_fact(f2)
                            
                            c = Contradiction(
                                conflict_id=f"CONF_{conflict_idx:03d}",
                                topic=f"Conflicting {topic.title()} Date",
                                statement_a=f1.text,
                                evidence_id_a=ev1.evidence_id if ev1 else "UNKNOWN",
                                doc_a=f1.document_id,
                                statement_b=f2.text,
                                evidence_id_b=ev2.evidence_id if ev2 else "UNKNOWN",
                                doc_b=f2.document_id,
                                contradiction_type="date_mismatch",
                                resolution_policy="DISCLOSE_CONFLICT_DO_NOT_RESOLVE"
                            )
                            contradictions.append(c)
                            conflict_idx += 1

        # 2. Financial Amount Contradictions
        amount_facts = []
        for f in facts:
            m = AMOUNT_EXTRACTION.search(f.text)
            if m:
                amount_facts.append((f, m.group(1).replace(",", "")))
                
        if len(amount_facts) >= 2:
            for i in range(len(amount_facts)):
                for j in range(i + 1, len(amount_facts)):
                    f1, amt1 = amount_facts[i]
                    f2, amt2 = amount_facts[j]
                    if amt1 != amt2 and f1.document_id != f2.document_id:
                        ev1 = self._find_evidence_for_fact(f1)
                        ev2 = self._find_evidence_for_fact(f2)
                        c = Contradiction(
                            conflict_id=f"CONF_{conflict_idx:03d}",
                            topic="Disputed Claim Amount",
                            statement_a=f1.text,
                            evidence_id_a=ev1.evidence_id if ev1 else "UNKNOWN",
                            doc_a=f1.document_id,
                            statement_b=f2.text,
                            evidence_id_b=ev2.evidence_id if ev2 else "UNKNOWN",
                            doc_b=f2.document_id,
                            contradiction_type="amount_conflict",
                            resolution_policy="DISCLOSE_CONFLICT_DO_NOT_RESOLVE"
                        )
                        contradictions.append(c)
                        conflict_idx += 1

        return contradictions

    def _find_date(self, text: str) -> str:
        m = DATE_EXTRACTION.search(text)
        return m.group(1).strip() if m else ""

    def _find_evidence_for_fact(self, fact: Fact) -> Evidence:
        for ev in self.ledger.list_evidence():
            if ev.source_id == fact.document_id and fact.text in ev.text_span:
                return ev
        # Fallback to any evidence matching document
        for ev in self.ledger.list_evidence():
            if ev.source_id == fact.document_id:
                return ev
        return None
