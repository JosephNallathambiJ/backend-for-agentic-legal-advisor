"""
core/case_parser.py - Case and Document Ingestion Engine
Performs page-aware text extraction, atomic fact segmentation, entity/date extraction,
and citation parsing with exact character offsets.
"""

import os
import re
from typing import List, Dict, Any, Tuple, Optional
from core.schemas import Fact
from core.provenance import EvidenceLedger
from core.security import SecurityManager
from core.logging_config import logger

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None

# Entity extraction patterns
ENTITY_PATTERNS = [
    (re.compile(r"(?:accused|applicant|petitioner)\s*(?:is|named|:)?\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)", re.IGNORECASE), "accused"),
    (re.compile(r"(?:complainant|informant|victim)\s*(?:is|named|:)?\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)", re.IGNORECASE), "complainant"),
    (re.compile(r"(?:police\s+station|ps)\s*[:\-]?\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)", re.IGNORECASE), "police_station"),
    (re.compile(r"(?:fir\s+no\.?|crime\s+no\.?)\s*[:\-]?\s*([A-Za-z0-9\/\-]+)", re.IGNORECASE), "fir_number"),
    (re.compile(r"(?:in\s+the\s+court\s+of|court)\s*[:\-]?\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)", re.IGNORECASE), "court"),
]

# Date patterns (e.g. 12 June 2024, 12.06.2024, 12/06/2024, 12th June)
DATE_PATTERN = re.compile(
    r"\b(?:\d{1,2}(?:st|nd|rd|th)?[\s\/\-\.](?:January|February|March|April|May|June|July|August|September|October|November|December|[0-9]{1,2})[\s\/\-\.]\d{2,4}|\d{1,2}(?:st|nd|rd|th)?\s+(?:January|February|March|April|May|June|July|August|September|October|November|December))\b",
    re.IGNORECASE
)

# Statutory citation patterns (supporting Section, Sec, Article, etc.)
CITATION_PATTERN = re.compile(
    r"\b(?:section|sec\.?|s\.|article|art\.?)\s*([0-9]+[A-Z0-9\-_]*)\s*(?:of\s+(?:the\s+)?)?((?:[A-Za-z0-9\s,\-_]*?\s+)?(?:Act|Sanhita|Adhiniyam|Code|BNS|BNSS|BSA|IPC|CrPC|CPC|GDPR|UCC|USC|PACE))\b",
    re.IGNORECASE
)

class CaseParser:
    def __init__(self, ledger: EvidenceLedger):
        self.ledger = ledger

    def parse_file(self, file_path: str, document_id: Optional[str] = None) -> Tuple[List[Fact], List[str], List[str]]:
        """
        Parses a document file (.pdf, .txt, .md).
        Returns:
            - List of atomic Fact objects
            - List of detected explicit statutory citations
            - List of security warnings
        """
        if not document_id:
            document_id = os.path.basename(file_path)

        valid, msg = SecurityManager.validate_file(file_path)
        if not valid:
            logger.warning(f"File validation warning for {file_path}: {msg}")
            return [], [], [msg]

        ext = os.path.splitext(file_path)[1].lower()
        pages_content: List[Tuple[int, str]] = []

        if ext == ".pdf":
            pages_content = self._extract_pdf_pages(file_path)
        else:
            with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
            pages_content = [(1, content)]

        return self.parse_pages_content(pages_content, document_id)

    def parse_text(self, text: str, document_id: str = "doc_inline") -> Tuple[List[Fact], List[str], List[str]]:
        """Parses inline raw text."""
        return self.parse_pages_content([(1, text)], document_id)

    def parse_pages_content(self, pages: List[Tuple[int, str]], document_id: str) -> Tuple[List[Fact], List[str], List[str]]:
        facts: List[Fact] = []
        citations_found: List[str] = []
        all_warnings: List[str] = []

        for page_num, raw_text in pages:
            sanitized_text, warnings = SecurityManager.sanitize_untrusted_text(raw_text)
            all_warnings.extend(warnings)

            # Extract citations from raw text
            for m in CITATION_PATTERN.finditer(sanitized_text):
                sec_num = m.group(1).strip()
                act_name = m.group(2).strip()
                cite_str = f"Section {sec_num} of {act_name}"
                if cite_str not in citations_found:
                    citations_found.append(cite_str)

            # Segment into atomic sentences / factual propositions
            sentences = self._split_into_propositions(sanitized_text)
            
            current_offset = 0
            for sent in sentences:
                sent_clean = sent.strip()
                if len(sent_clean) < 10:
                    continue

                start_idx = sanitized_text.find(sent_clean, current_offset)
                if start_idx == -1:
                    start_idx = current_offset
                end_idx = start_idx + len(sent_clean)
                current_offset = end_idx

                # Detect entities and dates in this sentence
                entity_detected = None
                for pat, ent_type in ENTITY_PATTERNS:
                    m = pat.search(sent_clean)
                    if m:
                        entity_detected = f"{ent_type}:{m.group(1).strip()}"
                        break

                date_detected = None
                date_m = DATE_PATTERN.search(sent_clean)
                if date_m:
                    date_detected = date_m.group(0).strip()

                fact = self.ledger.add_fact(
                    text=sent_clean,
                    document_id=document_id,
                    page=page_num,
                    offset_start=start_idx,
                    offset_end=end_idx,
                    extraction_method="case_parser_atomic_segmenter",
                    entity=entity_detected,
                    date_referenced=date_detected
                )
                facts.append(fact)

        return facts, citations_found, all_warnings

    def _extract_pdf_pages(self, pdf_path: str) -> List[Tuple[int, str]]:
        if not PdfReader:
            logger.error("pypdf is not available for PDF extraction.")
            return []
        pages = []
        try:
            reader = PdfReader(pdf_path)
            for idx, page in enumerate(reader.pages):
                text = page.extract_text() or ""
                pages.append((idx + 1, text))
        except Exception as e:
            logger.error(f"Error reading PDF {pdf_path}: {e}")
        return pages

    def _split_into_propositions(self, text: str) -> List[str]:
        """Splits narrative into atomic sentences while preserving dates, decimals, and abbreviations."""
        # Replace common abbreviations temporarily
        t = re.sub(r"\b(Mr|Mrs|Ms|Dr|Adv|Sec|No|para|vs|v)\.", r"\1<DOT>", text)
        sentences = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])|\n+", t)
        cleaned = [s.replace("<DOT>", ".").strip() for s in sentences if s.strip()]
        return cleaned
