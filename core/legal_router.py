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

# Explicit citation pattern supporting Section, Sec, Article, Art, Chapter, Ch, etc.
CITATION_EXTRACT_RE = re.compile(
    r"\b(?:section|sec\.?|s\.|article|art\.?|chapter|ch\.?)\s*([0-9]+[A-Z0-9\-_.:]*)\s*(?:of\s+(?:the\s+)?)?((?:[A-Za-z0-9\s,\-_]*?\s+)?(?:Act|Sanhita|Adhiniyam|Code|Constitution|Grundlov|Satversme|Konstitucija|Alaptörvény|Regeringsformen|Bunreacht|BNS|BNSS|BSA|IPC|CrPC|CPC|GDPR|UCC|USC|PACE))\b",
    re.IGNORECASE
)

# Canonical aliases across INDIA, US, UK, EU, and Northern & Eastern Europe
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
    
    # UNITED STATES
    "us constitution": "US_CONST_1787",
    "united states constitution": "US_CONST_1787",
    "constitution of the united states": "US_CONST_1787",
    "title 18": "US_TITLE_18",
    "18 usc": "US_TITLE_18",
    "18 u.s.c.": "US_TITLE_18",
    "ucc": "US_UCC_ART_2",
    "ucc article 2": "US_UCC_ART_2",
    "uniform commercial code": "US_UCC_ART_2",
    "civil rights act": "US_CIVIL_RIGHTS_1964",
    "civil rights act 1964": "US_CIVIL_RIGHTS_1964",
    "sherman act": "US_SHERMAN_1890",
    "sherman antitrust act": "US_SHERMAN_1890",
    "copyright act": "US_COPYRIGHT_1976",
    "us copyright act": "US_COPYRIGHT_1976",
    "title 28": "US_JUDICIARY_TITLE_28",
    "28 usc": "US_JUDICIARY_TITLE_28",
    "title 11": "US_BANKRUPTCY_TITLE_11",
    "11 usc": "US_BANKRUPTCY_TITLE_11",
    "bankruptcy code": "US_BANKRUPTCY_TITLE_11",
    "title 35": "US_PATENT_TITLE_35",
    "35 usc": "US_PATENT_TITLE_35",
    "patent act": "US_PATENT_TITLE_35",
    "securities exchange act": "US_SECURITIES_EXCHANGE_1934",
    "exchange act": "US_SECURITIES_EXCHANGE_1934",
    "ada": "US_ADA_1990",
    "americans with disabilities act": "US_ADA_1990",
    "foia": "US_FOIA_1966",
    "freedom of information act": "US_FOIA_1966",
    "apa": "US_APA_1946",
    "administrative procedure act": "US_APA_1946",
    "voting rights act": "US_VOTING_RIGHTS_1965",
    "clayton act": "US_CLAYTON_1914",
    "ftc act": "US_FTC_ACT_1914",
    "federal trade commission act": "US_FTC_ACT_1914",
    "securities act": "US_SECURITIES_1933",
    "securities act of 1933": "US_SECURITIES_1933",
    "dmca": "US_DMCA_1998",
    "digital millennium copyright act": "US_DMCA_1998",
    "lanham act": "US_LANHAM_ACT_1946",
    "trademark act": "US_LANHAM_ACT_1946",
    "flsa": "US_FLSA_1938",
    "fair labor standards act": "US_FLSA_1938",
    "osha": "US_OSHA_1970",
    "erisa": "US_ERISA_1974",
    "clean air act": "US_CLEAN_AIR_1970",
    "clean water act": "US_CLEAN_WATER_1972",
    "cercla": "US_CERCLA_1980",
    "superfund": "US_CERCLA_1980",
    "fdca": "US_FDCA_1938",
    "controlled substances act": "US_CSA_1970",
    "false claims act": "US_FALSE_CLAIMS_1863",
    "bank secrecy act": "US_BANK_SECRECY_1970",
    "dodd-frank": "US_DODD_FRANK_2010",
    "section 230": "US_COMMUNICATIONS_1934",
    "communications act": "US_COMMUNICATIONS_1934",
    "hipaa": "US_HIPAA_1996",
    
    # UNITED KINGDOM
    "theft act": "UK_THEFT_1968",
    "theft act 1968": "UK_THEFT_1968",
    "theft act 1978": "UK_THEFT_1978",
    "contracts rights of third parties": "UK_CONTRACTS_1999",
    "consumer rights act 2015": "UK_CONSUMER_2015",
    "human rights act 1998": "UK_HUMAN_RIGHTS_1998",
    "uk human rights act": "UK_HUMAN_RIGHTS_1998",
    "fraud act 2006": "UK_FRAUD_2006",
    "uk fraud act": "UK_FRAUD_2006",
    "forgery act": "UK_FORGERY_1981",
    "criminal justice act 2003": "UK_CRIMINAL_JUSTICE_2003",
    "data protection act 2018": "UK_DATA_PROTECTION_2018",
    "uk dpa 2018": "UK_DATA_PROTECTION_2018",
    "companies act 2006": "UK_COMPANIES_2006",
    "sale of goods act": "UK_SALE_OF_GOODS_1979",
    "supply of goods and services act": "UK_SUPPLY_OF_GOODS_1982",
    "ucta": "UK_UCTA_1977",
    "unfair contract terms act": "UK_UCTA_1977",
    "insolvency act 1986": "UK_INSOLVENCY_1986",
    "partnership act 1890": "UK_PARTNERSHIP_1890",
    "llp act": "UK_LLP_2000",
    "arbitration act 1996": "UK_ARBITRATION_1996",
    "uk arbitration act": "UK_ARBITRATION_1996",
    "employment rights act": "UK_EMPLOYMENT_RIGHTS_1996",
    "equality act": "UK_EQUALITY_2010",
    "equality act 2010": "UK_EQUALITY_2010",
    "pace": "UK_PACE_1984",
    "police and criminal evidence act": "UK_PACE_1984",
    "bribery act": "UK_BRIBERY_2010",
    "bribery act 2010": "UK_BRIBERY_2010",
    "poca": "UK_POCA_2002",
    "proceeds of crime act": "UK_POCA_2002",
    "fsma": "UK_FSMA_2000",
    "financial services and markets act": "UK_FSMA_2000",
    "defamation act 2013": "UK_DEFAMATION_2013",
    "environmental protection act 1990": "UK_ENV_PROTECTION_1990",
    "official secrets act": "UK_OFFICIAL_SECRETS_1989",
    "computer misuse act": "UK_COMPUTER_MISUSE_1990",
    "online safety act": "UK_ONLINE_SAFETY_2023",
    
    # EUROPEAN UNION
    "gdpr": "EU_GDPR_2016",
    "eu gdpr": "EU_GDPR_2016",
    "general data protection regulation": "EU_GDPR_2016",
    "ai act": "EU_AI_ACT_2024",
    "eu ai act": "EU_AI_ACT_2024",
    "digital services act": "EU_DSA_2022",
    "dsa": "EU_DSA_2022",
    "digital markets act": "EU_DMA_2022",
    "dma": "EU_DMA_2022",
    "tfeu": "EU_TFEU_2012",
    "treaty on the functioning of the european union": "EU_TFEU_2012",
    "eu charter": "EU_CHARTER_2012",
    "charter of fundamental rights": "EU_CHARTER_2012",
    "teu": "EU_TEU_2016",
    "treaty on european union": "EU_TEU_2016",
    "e-commerce directive": "EU_ECOMMERCE_2000",
    "ecommerce directive": "EU_ECOMMERCE_2000",
    "mica": "EU_MICA_2023",
    "markets in crypto assets": "EU_MICA_2023",
    "data governance act": "EU_DGA_2022",
    "dga": "EU_DGA_2022",
    "data act": "EU_DATA_ACT_2023",
    "cybersecurity act": "EU_CYBERSECURITY_2019",
    "eidas": "EU_EIDAS_2024",
    "nis 2": "EU_NIS2_DIR_2022",
    "nis2": "EU_NIS2_DIR_2022",
    "copyright dsm": "EU_COPYRIGHT_DSM_2019",
    "csddd": "EU_CSDDD_2024",
    "corporate sustainability due diligence": "EU_CSDDD_2024",
    "csrd": "EU_CSRD_2022",
    "consumer rights directive": "EU_CONSUMER_RIGHTS_2011",
    "digital content directive": "EU_DIGITAL_CONTENT_2019",
    "sale of goods directive": "EU_SALE_OF_GOODS_2019",
    "trade secrets directive": "EU_TRADE_SECRETS_2016",
    "product liability directive": "EU_PRODUCT_LIABILITY_1985",
    "brussels i": "EU_BRUSSELS_I_RECAST_2012",
    "brussels i recast": "EU_BRUSSELS_I_RECAST_2012",
    "rome i": "EU_ROME_I_2008",
    "rome ii": "EU_ROME_II_2007",
    "european insolvency regulation": "EU_INSOLVENCY_2015",
    "chips act": "EU_CHIPS_ACT_2023",
    "net-zero industry act": "EU_NET_ZERO_INDUSTRY_2024",

    # NORTHERN & EASTERN EUROPE
    "belarus constitution": "BY_CONST_1994",
    "constitution of belarus": "BY_CONST_1994",
    "bulgarian constitution": "BG_CONST_1991",
    "constitution of bulgaria": "BG_CONST_1991",
    "czech constitution": "CZ_CONST_1993",
    "constitution of the czech republic": "CZ_CONST_1993",
    "danish constitution": "DK_CONST_1953",
    "constitution of denmark": "DK_CONST_1953",
    "grundloven": "DK_CONST_1953",
    "estonian constitution": "EE_CONST_1992",
    "constitution of estonia": "EE_CONST_1992",
    "finnish constitution": "FI_CONST_1999",
    "constitution of finland": "FI_CONST_1999",
    "hungarian constitution": "HU_CONST_2011",
    "fundamental law of hungary": "HU_CONST_2011",
    "icelandic constitution": "IS_CONST_1944",
    "constitution of iceland": "IS_CONST_1944",
    "irish constitution": "IE_CONST_1937",
    "constitution of ireland": "IE_CONST_1937",
    "bunreacht na heireann": "IE_CONST_1937",
    "latvian constitution": "LV_CONST_1922",
    "constitution of latvia": "LV_CONST_1922",
    "satversme": "LV_CONST_1922",
    "lithuanian constitution": "LT_CONST_1992",
    "constitution of lithuania": "LT_CONST_1992",
    "norwegian constitution": "NO_CONST_1814",
    "constitution of norway": "NO_CONST_1814",
    "polish constitution": "PL_CONST_1997",
    "constitution of poland": "PL_CONST_1997",
    "romanian constitution": "RO_CONST_1991",
    "constitution of romania": "RO_CONST_1991",
    "russian constitution": "RU_CONST_1993",
    "constitution of russia": "RU_CONST_1993",
    "slovak constitution": "SK_CONST_1992",
    "constitution of slovakia": "SK_CONST_1992",
    "swedish constitution": "SE_CONST_1974",
    "constitution of sweden": "SE_CONST_1974",
    "regeringsformen": "SE_CONST_1974",
    "ukrainian constitution": "UA_CONST_1996",
    "constitution of ukraine": "UA_CONST_1996"
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
        """Heuristically infers jurisdiction from query terms, country names, or dial codes."""
        q_lower = query.lower()
        
        # Dial codes and country mappings
        country_mappings = [
            ("BELARUS", ["belarus", "+375", "minsk", "pravo.by"]),
            ("BULGARIA", ["bulgaria", "+359", "sofia", "bulgarian"]),
            ("CZECH_REPUBLIC", ["czech", "+420", "prague", "zakonyprolidi"]),
            ("DENMARK", ["denmark", "+45", "danish", "grundlov", "copenhagen"]),
            ("ESTONIA", ["estonia", "+372", "estonian", "tallinn", "pohiseadus"]),
            ("FINLAND", ["finland", "+358", "finnish", "helsinki", "perustuslaki"]),
            ("HUNGARY", ["hungary", "+36", "hungarian", "budapest", "alaptorveny"]),
            ("ICELAND", ["iceland", "+354", "icelandic", "reykjavik", "stjornarskra"]),
            ("IRELAND", ["ireland", "+353", "irish", "dublin", "bunreacht"]),
            ("LATVIA", ["latvia", "+371", "latvian", "riga", "satversme"]),
            ("LITHUANIA", ["lithuania", "+370", "lithuanian", "vilnius", "konstitucija"]),
            ("NORWAY", ["norway", "+47", "norwegian", "oslo", "grunnlov"]),
            ("POLAND", ["poland", "+48", "polish", "warsaw", "konstytucja"]),
            ("ROMANIA", ["romania", "+40", "romanian", "bucharest", "constitutia"]),
            ("RUSSIA", ["russia", "+7", "russian", "moscow", "konstitutsiya"]),
            ("SLOVAKIA", ["slovakia", "+421", "slovak", "bratislava", "ustava"]),
            ("SWEDEN", ["sweden", "+46", "swedish", "stockholm", "regeringsform"]),
            ("UKRAINE", ["ukraine", "+380", "ukrainian", "kyiv", "konstytutsiya"]),
            ("US", ["united states", "18 usc", "title 18", "ucc", "federal code", "u.s.", "us constitution"]),
            ("UK", ["united kingdom", "theft act 1968", "consumer rights act 2015", "uk law", "acts of parliament"]),
            ("EU", ["gdpr", "eu ai act", "regulation 2016/679", "regulation 2024/1689", "european", "eur-lex"])
        ]
        
        for jur, keywords in country_mappings:
            if any(k in q_lower for k in keywords):
                return jur
                
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

    def route_query(self, query: str) -> Tuple[str, List[str]]:
        """
        Convenience router returning (detected_jurisdiction, list_of_candidate_act_ids).
        """
        candidates = self.route_candidates(query)
        act_ids = [c["act_id"] for c in candidates]
        jur = candidates[0]["jurisdiction"] if candidates else self.detect_jurisdiction(query)
        return jur, act_ids
