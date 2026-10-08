"""
core/legal_router.py - Lightweight Multi-Jurisdiction Router
Routes queries across INDIA, US, UK, and EU (Europe).
Rule: Explicit citations get priority. TF-IDF provides candidates, never a legal verdict.
"""

import os
import json
import re
from typing import List, Dict, Any, Optional, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from core.logging_config import logger

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTRY_PATH = os.path.join(WORKSPACE_DIR, "data", "registry", "registry_index.json")

# Explicit citation pattern supporting Section, Sec, Article, Art, etc.
CITATION_EXTRACT_RE = re.compile(
    r"\b(?:section|sec\.?|s\.|article|art\.?)\s*([0-9]+[A-Z0-9\-_]*)\s*(?:of\s+(?:the\s+)?)?((?:[A-Za-z0-9\s,\-_]*?\s+)?(?:Act|Sanhita|Adhiniyam|Code|BNS|BNSS|BSA|IPC|CrPC|CPC|GDPR|UCC|USC|PACE))\b",
    re.IGNORECASE
)

# Canonical aliases across INDIA, US, UK, EU
CANONICAL_ALIASES = {
    # INDIA
    "bns": "BNS_2023",
    "bharatiya nyaya sanhita": "BNS_2023",
    "nyaya sanhita": "BNS_2023",
    "bnss": "BNSS_2023",
    "bharatiya nagarik suraksha sanhita": "BNSS_2023",
    "nagarik suraksha": "BNSS_2023",
    "bsa": "BSA_2023",
    "bharatiya sakshya adhiniyam": "BSA_2023",
    "sakshya adhiniyam": "BSA_2023",
    "ica": "ICA_1872",
    "contract act": "ICA_1872",
    "indian contract act": "ICA_1872",
    "cpc": "CPC_1908",
    "code of civil procedure": "CPC_1908",
    "it act": "IT_2000",
    "information technology act": "IT_2000",
    "consumer act": "CONSUMER_2019",
    "consumer protection act": "CONSUMER_2019",
    "arbitration act": "ARBITRATION_1996",
    
    # US
    "title 18": "US_TITLE_18",
    "18 usc": "US_TITLE_18",
    "18 u.s.c.": "US_TITLE_18",
    "ucc": "US_UCC_ART_2",
    "ucc article 2": "US_UCC_ART_2",
    "uniform commercial code": "US_UCC_ART_2",
    
    # UK
    "theft act": "UK_THEFT_1968",
    "theft act 1968": "UK_THEFT_1968",
    "contracts rights of third parties": "UK_CONTRACTS_1999",
    "consumer rights act 2015": "UK_CONSUMER_2015",
    
    # EU / EUROPE
    "gdpr": "EU_GDPR_2016",
    "eu gdpr": "EU_GDPR_2016",
    "general data protection regulation": "EU_GDPR_2016",
    "ai act": "EU_AI_ACT_2024",
    "eu ai act": "EU_AI_ACT_2024"
}

class LegalRouter:
    def __init__(self, registry_file: str = REGISTRY_PATH):
        self.registry_file = registry_file
        self.registry: Dict[str, Dict[str, Any]] = {}
        self.act_ids: List[str] = []
        self.corpus_texts: List[str] = []
        self.vectorizer: Optional[TfidfVectorizer] = None
        self.tfidf_matrix = None
        self._load_registry()

    def _load_registry(self):
        if not os.path.exists(self.registry_file):
            logger.warning(f"Registry file not found at {self.registry_file}")
            return
            
        with open(self.registry_file, "r", encoding="utf-8") as f:
            self.registry = json.load(f)
            
        self.act_ids = []
        self.corpus_texts = []
        for act_id, meta in self.registry.items():
            self.act_ids.append(act_id)
            aliases_str = " ".join(meta.get("aliases", []))
            jur = meta.get("jurisdiction", "INDIA")
            text = f"{meta.get('act_title', '')} {meta.get('short_name', '')} {aliases_str} {jur} {meta.get('year', '')}"
            self.corpus_texts.append(text)

        if self.corpus_texts:
            self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
            self.tfidf_matrix = self.vectorizer.fit_transform(self.corpus_texts)
            logger.info(f"LegalRouter initialized with {len(self.act_ids)} Acts across multi-jurisdictions.")

    def detect_jurisdiction(self, query: str) -> str:
        """Heuristically infers jurisdiction from query terms."""
        q_lower = query.lower()
        if any(k in q_lower for k in ["gdpr", "eu ai act", "regulation 2016/679", "regulation 2024/1689", "european"]):
            return "EU"
        if any(k in q_lower for k in ["title 18", "18 usc", "ucc", "united states", "federal code"]):
            return "US"
        if any(k in q_lower for k in ["theft act 1968", "consumer rights act 2015", "united kingdom", "uk law"]):
            return "UK"
        return "INDIA"

    def parse_explicit_citations(self, text: str) -> List[Tuple[str, str]]:
        """
        Extracts tuples of (act_id, section_number) for explicit citations mentioned in text.
        """
        results = []
        for m in CITATION_EXTRACT_RE.finditer(text):
            sec_num = m.group(1).strip()
            act_raw = (m.group(2) or "").strip().lower()
            
            matched_act_id = None
            if act_raw:
                for alias, aid in CANONICAL_ALIASES.items():
                    if alias in act_raw or act_raw in alias:
                        matched_act_id = aid
                        break
                if not matched_act_id:
                    for aid, meta in self.registry.items():
                        if meta.get("short_name", "").lower() in act_raw or act_raw in meta.get("act_title", "").lower():
                            matched_act_id = aid
                            break
                            
            if matched_act_id and sec_num:
                results.append((matched_act_id, sec_num))
        return results

    def route_candidates(self, query: str, top_k: int = 5, jurisdiction: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Routes a query using explicit citations first, then TF-IDF candidate ranking.
        """
        candidates = []
        seen_acts = set()

        # 1. Priority: Explicit Citations
        explicit_cites = self.parse_explicit_citations(query)
        for act_id, sec_num in explicit_cites:
            if act_id in self.registry and act_id not in seen_acts:
                meta = self.registry[act_id]
                candidates.append({
                    "act_id": act_id,
                    "act_title": meta.get("act_title"),
                    "target_section": sec_num,
                    "jurisdiction": meta.get("jurisdiction", "INDIA"),
                    "confidence_score": 1.0,
                    "source_method": "explicit_citation"
                })
                seen_acts.add(act_id)

        # 2. Check direct alias matches in query text
        q_lower = query.lower()
        for alias, act_id in CANONICAL_ALIASES.items():
            if re.search(r"\b" + re.escape(alias) + r"\b", q_lower):
                if act_id in self.registry and act_id not in seen_acts:
                    meta = self.registry[act_id]
                    candidates.append({
                        "act_id": act_id,
                        "act_title": meta.get("act_title"),
                        "target_section": None,
                        "jurisdiction": meta.get("jurisdiction", "INDIA"),
                        "confidence_score": 0.95,
                        "source_method": "alias_exact_match"
                    })
                    seen_acts.add(act_id)

        # 3. TF-IDF Lexical Candidate Search
        if self.vectorizer and self.tfidf_matrix is not None and len(candidates) < top_k:
            q_vec = self.vectorizer.transform([query])
            sims = cosine_similarity(q_vec, self.tfidf_matrix).flatten()
            top_indices = sims.argsort()[::-1]
            
            for idx in top_indices:
                if len(candidates) >= top_k:
                    break
                score = float(sims[idx])
                if score < 0.05:
                    break
                aid = self.act_ids[idx]
                meta = self.registry[aid]
                if aid not in seen_acts:
                    if jurisdiction and meta.get("jurisdiction") != jurisdiction:
                        continue
                    candidates.append({
                        "act_id": aid,
                        "act_title": meta.get("act_title"),
                        "target_section": None,
                        "jurisdiction": meta.get("jurisdiction", "INDIA"),
                        "confidence_score": round(score, 3),
                        "source_method": "tfidf_candidate_rank"
                    })
                    seen_acts.add(aid)

        return candidates
