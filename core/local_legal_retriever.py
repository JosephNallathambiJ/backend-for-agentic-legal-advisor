"""
core/local_legal_retriever.py - Local Legal Corpus SQLite Retriever
Fast, deterministic, cache-backed offline retrieval of statutory sections.
Registers all retrieved sections into EvidenceLedger with cryptographic SHA-256 hashes.
"""

import os
import sqlite3
import time
from typing import Optional, List, Dict, Any
from core.schemas import Evidence
from core.provenance import EvidenceLedger
from core.logging_config import logger

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SQLITE_DB = os.path.join(WORKSPACE_DIR, "data", "cache", "legal_cache.sqlite")

class LocalLegalRetriever:
    def __init__(self, ledger: EvidenceLedger, db_path: str = SQLITE_DB):
        self.ledger = ledger
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        if not os.path.exists(self.db_path):
            logger.warning(f"SQLite DB not found at {self.db_path}. Run build_index.py first.")

    def lookup_section(self, act_id: str, section_number: str) -> Optional[Evidence]:
        """
        Retrieves a section by Act ID and Section Number.
        Returns Evidence object registered in EvidenceLedger, or None if not found.
        """
        if not os.path.exists(self.db_path):
            return None

        # Clean section number
        clean_sec = section_number.strip().upper()
        
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        
        # Query section with act info
        cur.execute("""
            SELECT s.section_id, s.act_id, a.act_title, s.section_number, s.title, s.text, s.source_url, s.sha256, COALESCE(s.jurisdiction, a.jurisdiction, 'INDIA')
            FROM sections s
            JOIN acts a ON s.act_id = a.act_id
            WHERE s.act_id = ? AND s.section_number = ?
            LIMIT 1
        """, (act_id, clean_sec))
        
        row = cur.fetchone()
        conn.close()

        if not row:
            return None

        sec_id, aid, act_title, sec_num, sec_title, sec_text, source_url, sec_hash, jur = row
        
        # Register in EvidenceLedger
        evidence = self.ledger.add_statute_evidence(
            act_id=aid,
            act_title=act_title,
            section_number=sec_num,
            text=sec_text,
            source_url=source_url or "https://indiacode.nic.in",
            version="official_local_snapshot",
            jurisdiction=jur
        )
        return evidence

    def search_sections_by_keyword(self, query: str, act_id: Optional[str] = None, limit: int = 5) -> List[Evidence]:
        """
        Searches sections containing keywords within the text or title.
        """
        if not os.path.exists(self.db_path):
            return []

        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        
        sql = """
            SELECT s.section_id, s.act_id, a.act_title, s.section_number, s.title, s.text, s.source_url, s.sha256, COALESCE(s.jurisdiction, a.jurisdiction, 'INDIA')
            FROM sections s
            JOIN acts a ON s.act_id = a.act_id
            WHERE (s.text LIKE ? OR s.title LIKE ?)
        """
        params = [f"%{query}%", f"%{query}%"]
        
        if act_id:
            sql += " AND s.act_id = ?"
            params.append(act_id)
            
        sql += f" LIMIT {limit}"
        
        cur.execute(sql, tuple(params))
        rows = cur.fetchall()
        conn.close()

        results = []
        for row in rows:
            sec_id, aid, act_title, sec_num, sec_title, sec_text, source_url, sec_hash, jur = row
            evidence = self.ledger.add_statute_evidence(
                act_id=aid,
                act_title=act_title,
                section_number=sec_num,
                text=sec_text,
                source_url=source_url or "https://indiacode.nic.in",
                version="official_local_snapshot",
                jurisdiction=jur
            )
            results.append(evidence)
            
        return results
