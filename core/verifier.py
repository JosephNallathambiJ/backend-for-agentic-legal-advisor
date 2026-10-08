"""
core/verifier.py - Deterministic Zero-Fabrication Verification Engine
Executes independent verification gates:
  - Check A: Schema Validation
  - Check B: Citation Allowlist
  - Check C: Exact Quotation Matching
  - Check D: Claim / Evidence Alignment
  - Check E: Fact-Source Check (Case facts vs Statutes)
  - Check F: Legal Applicability & Versioning
  - Check G: NLI Semantic Alignment
  - Check H: Fail-Closed Release
Enforces: The LLM NEVER sets its own verdict. Only the Verifier assigns PASS / FLAG / REJECT.
"""

import re
from typing import List, Dict, Tuple, Optional
from core.schemas import Claim, Verdict, Evidence
from core.provenance import EvidenceLedger
from core.nli_verifier import NLIVerifier
from core.logging_config import logger

class DeterministicVerifier:
    def __init__(self, ledger: EvidenceLedger, nli_verifier: Optional[NLIVerifier] = None):
        self.ledger = ledger
        self.nli = nli_verifier or NLIVerifier()

    @staticmethod
    def normalize_for_quote_match(text: str) -> str:
        """Controlled normalization of whitespace, line breaks, and typographical punctuation."""
        t = re.sub(r'[\u201c\u201d"]', '"', text)
        t = re.sub(r"[\u2018\u2019']", "'", t)
        t = re.sub(r"[—–\-]", "-", t)
        t = re.sub(r"\s+", " ", t)
        return t.strip()

    def verify_claim(self, claim: Claim) -> Verdict:
        """
        Executes Checks A through H on an individual atomic claim.
        Returns a definitive typed Verdict.
        """
        checks: Dict[str, bool] = {
            "schema_valid": False,
            "citations_allowed": False,
            "quotes_authentic": False,
            "evidence_aligned": False,
            "fact_source_valid": False,
            "applicability_valid": False,
            "nli_entailed": False
        }
        reason_codes: List[str] = []

        try:
            # ---------------------------------------------------------
            # Check A: Output Schema Validation
            # ---------------------------------------------------------
            if not claim.claim_id or not claim.text:
                return Verdict(
                    claim_id=claim.claim_id or "UNKNOWN",
                    status="REJECT",
                    reason_codes=["ERR_SCHEMA_MALFORMED"],
                    checks=checks,
                    reviewer_required=True,
                    audit_notes="Malformed claim object: missing claim_id or text"
                )
            checks["schema_valid"] = True

            # If claim has no evidence mapped -> REJECT immediately
            if not claim.evidence_ids:
                return Verdict(
                    claim_id=claim.claim_id,
                    status="REJECT",
                    reason_codes=["ERR_NO_EVIDENCE_MAPPED"],
                    checks=checks,
                    reviewer_required=True,
                    audit_notes="Non-negotiable rule: No evidence -> No asserted claim"
                )

            # Retrieve mapped evidence records
            mapped_evidences: List[Evidence] = []
            for ev_id in claim.evidence_ids:
                ev = self.ledger.get_evidence(ev_id)
                if not ev:
                    reason_codes.append(f"ERR_EVIDENCE_NOT_FOUND:{ev_id}")
                else:
                    mapped_evidences.append(ev)

            if not mapped_evidences:
                return Verdict(
                    claim_id=claim.claim_id,
                    status="REJECT",
                    reason_codes=reason_codes or ["ERR_UNRESOLVED_EVIDENCE_IDS"],
                    checks=checks,
                    reviewer_required=True,
                    audit_notes="Referenced evidence IDs do not exist in ledger"
                )

            # ---------------------------------------------------------
            # Check B: Citation Allowlist
            # ---------------------------------------------------------
            citation_issues = []
            if claim.citation_ids:
                for cite_id in claim.citation_ids:
                    matched = False
                    for ev in mapped_evidences:
                        if ev.evidence_type == "statute" and (cite_id.lower() in ev.locator.lower() or cite_id.lower() in ev.source_id.lower()):
                            matched = True
                            break
                    if not matched:
                        citation_issues.append(f"UNVERIFIED_CITATION:{cite_id}")

            sec_mentions = re.findall(r"\b(?:section|article|sec\.?|art\.?)\s*([0-9]+[A-Z0-9\-_]*)\b", claim.text, re.IGNORECASE)
            for sm in sec_mentions:
                is_citing_statute = (
                    claim.claim_type == "statutory" or
                    any(term in claim.text.lower() for term in [
                        "bns", "bnss", "bsa", "act", "sanhita", "code", "adhiniyam",
                        "gdpr", "ucc", "usc", "regulation", "title", "theft act"
                    ])
                )
                if is_citing_statute:
                    statute_found = False
                    for ev in self.ledger.list_evidence():
                        if ev.evidence_type == "statute":
                            # Check exact section or Act title naming
                            if ev.section == sm or (ev.source_title and f"Article {sm}" in ev.source_title):
                                statute_found = True
                                break
                    if not statute_found:
                        citation_issues.append(f"ERR_CITATION_NOT_IN_LOCAL_CORPUS:Sec{sm}")

            if citation_issues:
                reason_codes.extend(citation_issues)
                return Verdict(
                    claim_id=claim.claim_id,
                    status="REJECT",
                    reason_codes=reason_codes,
                    checks=checks,
                    reviewer_required=True,
                    audit_notes="Citation allowlist failure: fabricated or unverified statutory citation"
                )
            checks["citations_allowed"] = True

            # ---------------------------------------------------------
            # Check C: Exact Quotation Validation
            # ---------------------------------------------------------
            quotes = re.findall(r'["“]([^"”]{5,})["”]', claim.text)
            quote_rejected = False
            for q in quotes:
                norm_quote = self.normalize_for_quote_match(q)
                matched_in_any = False
                for ev in mapped_evidences:
                    norm_ev = self.normalize_for_quote_match(ev.text_span)
                    if norm_quote in norm_ev:
                        matched_in_any = True
                        break
                if not matched_in_any:
                    quote_rejected = True
                    reason_codes.append(f"ERR_ALTERED_OR_FABRICATED_QUOTE:\"{q[:30]}...\"")

            if quote_rejected:
                return Verdict(
                    claim_id=claim.claim_id,
                    status="REJECT",
                    reason_codes=reason_codes,
                    checks=checks,
                    reviewer_required=True,
                    audit_notes="Quotation does not match source evidence text exactly"
                )
            checks["quotes_authentic"] = True

            # ---------------------------------------------------------
            # Check E: Fact-Source Verification
            # Case facts must cite case dossier evidence, NOT statutes!
            # ---------------------------------------------------------
            if claim.claim_type == "factual":
                has_case_evidence = any(ev.evidence_type == "case_fact" for ev in mapped_evidences)
                if not has_case_evidence:
                    reason_codes.append("ERR_FACT_SOURCE_MISMATCH:Statute_cannot_prove_case_occurrence")
                    return Verdict(
                        claim_id=claim.claim_id,
                        status="REJECT",
                        reason_codes=reason_codes,
                        checks=checks,
                        reviewer_required=True,
                        audit_notes="Factual case allegation cited against statutory authority without case evidence"
                    )
            checks["fact_source_valid"] = True

            # ---------------------------------------------------------
            # Check F: Applicability & Version Checks
            # ---------------------------------------------------------
            applicability_warning = False
            for ev in mapped_evidences:
                if ev.evidence_type == "statute" and "BNS" in ev.source_id:
                    for case_ev in self.ledger.list_evidence():
                        if case_ev.evidence_type == "case_fact" and re.search(r"\b(?:2021|2022|2023|prior to 2024)\b", case_ev.text_span):
                            applicability_warning = True
                            reason_codes.append("WARN_TRANSITION_APPLICABILITY:Pre_July_2024_offences_may_govern_IPC")
                            break

            checks["applicability_valid"] = not applicability_warning

            # ---------------------------------------------------------
            # Check G: NLI / Semantic Alignment Check
            # ---------------------------------------------------------
            combined_evidence_text = "\n".join([ev.text_span for ev in mapped_evidences])
            evidence_metadata = " ".join([f"{ev.source_title} {ev.locator} {ev.section or ''} {ev.jurisdiction}" for ev in mapped_evidences])
            
            # If claim is an authentic quotation directly verified by Check C
            if claim.is_quote and checks["quotes_authentic"]:
                nli_res = "ENTAILMENT_CONFIDENT"
                nli_exp = "Verbatim verified quotation"
            else:
                nli_res, nli_conf, nli_exp = self.nli.check_entailment(
                    premise=combined_evidence_text,
                    hypothesis=claim.text,
                    metadata=evidence_metadata
                )

            if nli_res == "CONTRADICTION":
                reason_codes.append(f"ERR_NLI_CONTRADICTION:{nli_exp}")
                return Verdict(
                    claim_id=claim.claim_id,
                    status="REJECT",
                    reason_codes=reason_codes,
                    checks=checks,
                    reviewer_required=True,
                    audit_notes="Semantic contradiction detected between claim and cited evidence"
                )
            elif nli_res == "ENTAILMENT_CONFIDENT":
                checks["nli_entailed"] = True
                checks["evidence_aligned"] = True
            else: # UNCERTAIN
                reason_codes.append(f"WARN_NLI_UNCERTAIN:{nli_exp}")
                checks["evidence_aligned"] = False
                checks["nli_entailed"] = False

            # ---------------------------------------------------------
            # Check H: Final Release Decision
            # ---------------------------------------------------------
            if checks["schema_valid"] and checks["citations_allowed"] and checks["quotes_authentic"] and checks["fact_source_valid"] and checks["evidence_aligned"] and checks["applicability_valid"]:
                return Verdict(
                    claim_id=claim.claim_id,
                    status="PASS",
                    reason_codes=["VERIFIED_SUPPORTED"],
                    checks=checks,
                    reviewer_required=False,
                    audit_notes="All independent verification gates passed."
                )
            else:
                return Verdict(
                    claim_id=claim.claim_id,
                    status="FLAG",
                    reason_codes=reason_codes or ["FLAG_INSUFFICIENT_CONFIDENCE"],
                    checks=checks,
                    reviewer_required=True,
                    audit_notes="Claim contains uncertainties or partial support requiring human review."
                )

        except Exception as ex:
            logger.error(f"Verifier crashed on claim {claim.claim_id}: {ex}")
            return Verdict(
                claim_id=claim.claim_id,
                status="REJECT",
                reason_codes=["FAIL_CLOSED_EXCEPTION"],
                checks=checks,
                reviewer_required=True,
                audit_notes=f"Internal verifier crash fail-closed: {str(ex)}"
            )

    def verify_all(self, claims: List[Claim]) -> List[Verdict]:
        return [self.verify_claim(c) for c in claims]
