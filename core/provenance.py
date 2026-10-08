"""
core/provenance.py - Thread-safe Evidence Ledger of Record
Preserves provenance IDs, source spans, document locations, and cryptographic SHA-256 hashes.
"""

import hashlib
import threading
from typing import Dict, List, Optional
from core.schemas import Evidence, Fact

class EvidenceLedger:
    def __init__(self):
        self._lock = threading.Lock()
        self._evidence: Dict[str, Evidence] = {}
        self._facts: Dict[str, Fact] = {}
        self._evidence_counter = 1
        self._fact_counter = 1

    @staticmethod
    def compute_hash(text: str) -> str:
        return hashlib.sha256(text.strip().encode("utf-8")).hexdigest()

    def add_fact(
        self,
        text: str,
        document_id: str,
        page: int = 1,
        offset_start: int = 0,
        offset_end: int = 0,
        extraction_method: str = "case_parser",
        entity: Optional[str] = None,
        date_referenced: Optional[str] = None
    ) -> Fact:
        with self._lock:
            fact_id = f"F{self._fact_counter:04d}"
            self._fact_counter += 1
            fact = Fact(
                fact_id=fact_id,
                text=text.strip(),
                document_id=document_id,
                page=page,
                character_offset_start=offset_start,
                character_offset_end=offset_end,
                extraction_method=extraction_method,
                entity=entity,
                date_referenced=date_referenced
            )
            self._facts[fact_id] = fact
            
            # Automatically create an evidence record for this case fact
            ev_id = f"E{self._evidence_counter:04d}"
            self._evidence_counter += 1
            evidence = Evidence(
                evidence_id=ev_id,
                evidence_type="case_fact",
                source_id=document_id,
                source_title=f"Uploaded Dossier: {document_id}",
                source_path=document_id,
                page=page,
                text_span=text.strip(),
                locator=f"{document_id}:p{page}:char{offset_start}-{offset_end}",
                version="case_upload_v1",
                hash=self.compute_hash(text)
            )
            self._evidence[ev_id] = evidence
            return fact

    def add_statute_evidence(
        self,
        act_id: str,
        act_title: str,
        section_number: str,
        text: str,
        source_url: str,
        version: str = "official_local_snapshot",
        jurisdiction: str = "INDIA"
    ) -> Evidence:
        with self._lock:
            # Check if this exact statute section is already recorded
            locator = f"{act_id}:Sec{section_number}"
            for ev in self._evidence.values():
                if ev.locator == locator:
                    return ev

            ev_id = f"E{self._evidence_counter:04d}"
            self._evidence_counter += 1
            evidence = Evidence(
                evidence_id=ev_id,
                evidence_type="statute",
                jurisdiction=jurisdiction,
                source_id=act_id,
                source_title=act_title,
                source_path=source_url,
                section=section_number,
                text_span=text.strip(),
                locator=locator,
                version=version,
                hash=self.compute_hash(text)
            )
            self._evidence[ev_id] = evidence
            return evidence

    def get_evidence(self, evidence_id: str) -> Optional[Evidence]:
        return self._evidence.get(evidence_id)

    def get_evidence_by_locator(self, locator: str) -> Optional[Evidence]:
        for ev in self._evidence.values():
            if ev.locator.lower() == locator.lower():
                return ev
        return None

    def get_fact(self, fact_id: str) -> Optional[Fact]:
        return self._facts.get(fact_id)

    def list_evidence(self) -> List[Evidence]:
        return list(self._evidence.values())

    def list_facts(self) -> List[Fact]:
        return list(self._facts.values())

    def clear(self):
        with self._lock:
            self._evidence.clear()
            self._facts.clear()
            self._evidence_counter = 1
            self._fact_counter = 1
