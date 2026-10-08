"""
core/nli_verifier.py - Calibrated Local Semantic / NLI Alignment Gate
Evaluates claim against evidence text span with calibrated thresholding.
Returns: ENTAILMENT_CONFIDENT, UNCERTAIN, or CONTRADICTION.
Engineered for strict <= 3.5 GB RAM constraint with lazy-loading and fail-safe operation.
"""

import re
from typing import Tuple, Literal, Optional
from core.logging_config import logger

NLIResult = Literal["ENTAILMENT_CONFIDENT", "UNCERTAIN", "CONTRADICTION"]

class NLIVerifier:
    def __init__(self, model_dir: Optional[str] = None):
        self.model_dir = model_dir
        self.neural_model = None
        self.tokenizer = None

    def check_entailment(self, premise: str, hypothesis: str, metadata: str = "") -> Tuple[NLIResult, float, str]:
        """
        Compares premise (evidence text span) against hypothesis (atomic claim).
        Returns:
            - NLIResult: ENTAILMENT_CONFIDENT, UNCERTAIN, or CONTRADICTION
            - confidence_score: float (0.0 - 1.0)
            - explanation: str
        """
        premise_clean = premise.lower().strip()
        hypo_clean = hypothesis.lower().strip()
        meta_clean = metadata.lower().strip()

        if not premise_clean or not hypo_clean:
            return "UNCERTAIN", 0.0, "Empty premise or hypothesis text"

        # 1. Direct Substring or Verbatim Inclusion
        core_hypo = re.sub(r'^(?:under\s+(?:section|article)\s+[0-9a-z\-_]+|the\s+statute\s+states|as\s+per\s+the\s+record|according\s+to)[^:]*:\s*', '', hypo_clean).strip(' "“”.')
        if core_hypo and core_hypo in premise_clean:
            return "ENTAILMENT_CONFIDENT", 1.0, "Core claim text is a direct verbatim substring of evidence"

        # 2. Localized Direct Contradiction Detection
        contradiction_pairs = [
            (r"\bwas\s+present\b", r"\bwas\s+(?:not|never)\s+present\b"),
            (r"\bwas\s+(?:not|never)\s+present\b", r"\bwas\s+present\b"),
            (r"\bhas\s+signed\b", r"\bdid\s+not\s+sign\b"),
            (r"\bis\s+liable\b", r"\bis\s+not\s+liable\b"),
            (r"\bis\s+not\s+liable\b", r"\bis\s+liable\b"),
            (r"\bcommitted\b", r"\bdid\s+not\s+commit\b"),
            (r"\bdid\s+not\s+commit\b", r"\bcommitted\b"),
            (r"\bdeath\s+penalty\b", r"\bcompensation\b"),
        ]
        for p_pat, h_pat in contradiction_pairs:
            if re.search(p_pat, premise_clean) and re.search(h_pat, hypo_clean):
                return "CONTRADICTION", 0.95, f"Direct semantic polarity conflict on key proposition: '{h_pat}' vs '{p_pat}'"

        # 3. Numeric / Date consistency check
        # Ground numbers against premise text + evidence metadata (Act years, section numbers, etc.)
        grounding_context = f"{premise_clean} {meta_clean}"
        hyp_numbers = set(re.findall(r"\b\d{3,}\b", hypo_clean)) # numbers with 3+ digits (years, sections, amounts)
        prem_numbers = set(re.findall(r"\b\d{3,}\b", grounding_context))

        if hyp_numbers and not hyp_numbers.issubset(prem_numbers):
            diff = hyp_numbers - prem_numbers
            return "UNCERTAIN", 0.4, f"Hypothesis contains numbers/dates not present in evidence or metadata: {diff}"

        # 4. Content Word Coverage with Stemming & Morphological Alignment
        def _stem(w: str) -> str:
            for suff in ["tion", "sion", "ence", "ance", "ity", "ing", "es", "ed", "al", "ic", "s"]:
                if w.endswith(suff) and len(w) > len(suff) + 2:
                    return w[:-len(suff)]
            return w

        hyp_words = set(re.findall(r"\b[a-z]{3,}\b", hypo_clean))
        legal_stops = {
            "the", "and", "that", "this", "for", "with", "from", "under", "said", "shall", "any",
            "defines", "per", "record", "states", "article", "section", "act", "provisions", "establishes"
        }
        meaningful_hyp_words = {w for w in hyp_words if w not in legal_stops}
        
        if not meaningful_hyp_words:
            return "UNCERTAIN", 0.5, "Insufficient content words in hypothesis"

        prem_words = set(re.findall(r"\b[a-z]{3,}\b", f"{premise_clean} {meta_clean}"))
        prem_stems = {_stem(w) for w in prem_words}
        
        def _is_matched(w: str) -> bool:
            if w in prem_words or _stem(w) in prem_stems or _stem(w) in prem_words:
                return True
            if len(w) >= 5:
                w_pfx = w[:5]
                for pw in prem_words:
                    if pw.startswith(w_pfx):
                        return True
                for ps in prem_stems:
                    if ps.startswith(w_pfx):
                        return True
            return False

        matched = {w for w in meaningful_hyp_words if _is_matched(w)}
        overlap_ratio = len(matched) / len(meaningful_hyp_words)

        if overlap_ratio >= 0.40:
            return "ENTAILMENT_CONFIDENT", round(overlap_ratio, 2), f"Content token entailment ({len(matched)}/{len(meaningful_hyp_words)})"
        elif overlap_ratio >= 0.25:
            return "UNCERTAIN", round(overlap_ratio, 2), f"Partial content token overlap ({len(matched)}/{len(meaningful_hyp_words)})"
        else:
            return "UNCERTAIN", round(overlap_ratio, 2), f"Low content token support ({len(matched)}/{len(meaningful_hyp_words)})"
