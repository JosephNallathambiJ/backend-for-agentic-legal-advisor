"""
core/agent_orchestrator.py - Bounded Deterministic Agent Orchestrator
Controls the reasoning loop with strict budgets, pre-draft audits, bounded tools,
and fail-closed release gates.
Rule: Retrieval and verification are deterministic services. The LLM never marks its own output as verified.
"""

import time
from typing import List, Dict, Any, Optional
from core.schemas import PreDraftAudit, StructuredDraft, PipelineResult, Verdict, Claim, Evidence
from core.provenance import EvidenceLedger
from core.case_parser import CaseParser
from core.legal_router import LegalRouter
from core.local_legal_retriever import LocalLegalRetriever
from core.contradiction_detector import ContradictionDetector
from core.verifier import DeterministicVerifier
from core.llm_engine import LocalLLMEngine
from core.telemetry import LocalTelemetryTracker
from core.logging_config import logger

MAX_TOOL_CALLS = 10
MAX_PLANNING_STEPS = 5

class AgentOrchestrator:
    def __init__(
        self,
        ledger: Optional[EvidenceLedger] = None,
        retriever: Optional[LocalLegalRetriever] = None,
        router: Optional[LegalRouter] = None,
        verifier: Optional[DeterministicVerifier] = None,
        llm_engine: Optional[LocalLLMEngine] = None
    ):
        self.ledger = ledger or EvidenceLedger()
        self.retriever = retriever or LocalLegalRetriever(self.ledger)
        self.router = router or LegalRouter()
        self.verifier = verifier or DeterministicVerifier(self.ledger)
        self.llm = llm_engine or LocalLLMEngine()
        self.parser = CaseParser(self.ledger)
        self.contradiction_detector = ContradictionDetector(self.ledger)

    def execute_workflow(
        self,
        workflow: str,
        query: str,
        document_paths: Optional[List[str]] = None,
        raw_text_dossier: Optional[str] = None
    ) -> PipelineResult:
        """
        Executes bounded pipeline:
        1. Intake & Parse documents
        2. Detect Contradictions
        3. Local Legal Retrieval (Priority citations -> TF-IDF candidates)
        4. Case Confidence Audit (Pre-Draft)
        5. Structured Drafting
        6. Deterministic Verification
        7. Fail-Closed Release Filtering
        """
        telemetry = LocalTelemetryTracker()
        tool_call_count = 0

        # Step 1: Intake & Parse documents into EvidenceLedger
        t0 = time.time()
        explicit_cites_found: List[str] = []
        
        if document_paths:
            for path in document_paths:
                facts, cites, warnings = self.parser.parse_file(path)
                explicit_cites_found.extend(cites)
                tool_call_count += 1
                
        if raw_text_dossier:
            facts, cites, warnings = self.parser.parse_text(raw_text_dossier, document_id="case_dossier_text")
            explicit_cites_found.extend(cites)
            tool_call_count += 1

        # Also parse explicit citations from query itself
        query_cites = self.router.parse_explicit_citations(query)
        for act_id, sec_num in query_cites:
            explicit_cites_found.append(f"Section {sec_num} of {act_id}")

        # Step 2: Detect Contradictions across facts
        contradictions = self.contradiction_detector.detect_contradictions()

        # Step 3: Local Legal Retrieval
        retrieval_start = time.time()
        retrieved_statute_evidences: List[Evidence] = []

        # 3a. Retrieve explicitly cited statutes first
        for act_id, sec_num in query_cites:
            if tool_call_count >= MAX_TOOL_CALLS:
                break
            ev = self.retriever.lookup_section(act_id, sec_num)
            tool_call_count += 1
            if ev:
                retrieved_statute_evidences.append(ev)
                telemetry.record_retrieval(1.5, hit=True)
            else:
                telemetry.record_retrieval(1.5, hit=False)

        # 3b. Retrieve candidate acts via Legal Router
        detected_jur = self.router.detect_jurisdiction(query)
        candidates = self.router.route_candidates(query, top_k=3, jurisdiction=detected_jur)
        for cand in candidates:
            if tool_call_count >= MAX_TOOL_CALLS:
                break
            aid = cand["act_id"]
            target_sec = cand.get("target_section")
            if target_sec:
                ev = self.retriever.lookup_section(aid, target_sec)
                tool_call_count += 1
                if ev:
                    retrieved_statute_evidences.append(ev)
            else:
                sec_evs = self.retriever.search_sections_by_keyword(query[:30], act_id=aid, limit=2)
                tool_call_count += 1
                retrieved_statute_evidences.extend(sec_evs)

        # Step 4: Pre-Draft Audit (Case Confidence Audit)
        facts = self.ledger.list_facts()
        known_facts = [f.text for f in facts]
        
        missing_info = []
        questions = []
        risks = []
        
        if not facts and workflow in ["contract_case_review", "legal_drafting"]:
            missing_info.append("No case document uploaded. All case-specific allegations must be withheld.")
            risks.append("High drafting risk: lack of uploaded factual record.")

        # Check for missing essential details in bail/drafting
        if workflow in ["legal_drafting", "bail_petition"]:
            has_fir = any("fir" in f.lower() for f in known_facts)
            has_arrest_date = any(f.date_referenced for f in facts if "arrest" in f.text.lower())
            if not has_fir:
                missing_info.append("FIR Number not found in uploaded case record.")
                questions.append("What is the formal FIR / Crime Number registered?")
            if not has_arrest_date:
                missing_info.append("Date of arrest / custody not specified in source.")
                questions.append("When was the applicant taken into judicial/police custody?")

        if contradictions:
            risks.append(f"Detected {len(contradictions)} factual contradictions across records.")
            for c in contradictions:
                questions.append(f"Clarification required for {c.topic}: '{c.statement_a}' vs '{c.statement_b}'")

        audit = PreDraftAudit(
            known_facts=known_facts[:10],
            unknown_facts=missing_info,
            conflicting_facts=contradictions,
            explicit_citations=explicit_cites_found,
            candidate_statutes=candidates,
            unavailable_evidence=[m for m in missing_info],
            questions_for_counsel=questions,
            drafting_risks=risks
        )

        # Step 5: Structured Drafting
        llm_t0 = time.time()
        approved_evidence_bundle = self.ledger.list_evidence()
        
        # If Grounded RAG Chat with no evidence -> ABSTAIN directly
        if workflow == "rag_chat" and not approved_evidence_bundle:
            draft = StructuredDraft(
                task_type=workflow,
                title="ABSTENTION: NOT_VERIFIED",
                claims=[],
                missing_information=["No evidence available in local legal corpus or case dossier."],
                uncertainties=["Abstention triggered under verifiability over fluency requirement."],
                draft_text="NOT_VERIFIED: Insufficient local evidence to ground this claim."
            )
            telemetry.record_llm(1.0)
            return PipelineResult(
                workflow=workflow,
                query_or_task=query,
                pre_draft_audit=audit,
                structured_draft=draft,
                claims=[],
                verdicts=[],
                evidence_records=[],
                contradictions=contradictions,
                telemetry=telemetry.get_report(),
                final_audited_text=draft.draft_text
            )

        draft = self.llm.draft(
            task_type=workflow,
            query=query,
            approved_evidence=approved_evidence_bundle,
            known_facts=known_facts,
            missing_information=missing_info
        )
        telemetry.record_llm((time.time() - llm_t0) * 1000.0)

        # Step 6: Deterministic Verification of Claims
        v_t0 = time.time()
        verdicts = self.verifier.verify_all(draft.claims)
        telemetry.record_verification((time.time() - v_t0) * 1000.0)

        # Attach verdicts to draft
        draft.verdicts = {v.claim_id: v for v in verdicts}

        # Step 7: Fail-Closed Release Filtering
        final_text = self._build_audited_release(draft, verdicts)

        return PipelineResult(
            workflow=workflow,
            query_or_task=query,
            pre_draft_audit=audit,
            structured_draft=draft,
            claims=draft.claims,
            verdicts=verdicts,
            evidence_records=self.ledger.list_evidence(),
            contradictions=contradictions,
            telemetry=telemetry.get_report(),
            final_audited_text=final_text
        )

    def _build_audited_release(self, draft: StructuredDraft, verdicts: List[Verdict]) -> str:
        """
        Builds the final rendered text conforming to the release rule:
        PASS claims are presented as verified.
        FLAG claims are rendered with explicit uncertainty warnings.
        REJECT claims are WITHHELD or struck out with reason codes.
        """
        lines = [f"# {draft.title}\n"]
        
        pass_count = sum(1 for v in verdicts if v.status == "PASS")
        flag_count = sum(1 for v in verdicts if v.status == "FLAG")
        reject_count = sum(1 for v in verdicts if v.status == "REJECT")
        
        lines.append(f"> **AUDIT SUMMARY**: {pass_count} VERIFIED (PASS) | {flag_count} FLAGGED | {reject_count} REJECTED/WITHHELD\n")
        
        # Include draft court header and placeholders if present
        if "IN THE COURT OF:" in draft.draft_text:
            parts = draft.draft_text.split("MOST RESPECTFULLY SHOWETH:")
            lines.append(parts[0].strip() + "\n\nMOST RESPECTFULLY SHOWETH:\n")

        # Render verified and flagged sections
        for claim in draft.claims:
            v = draft.verdicts.get(claim.claim_id)
            if not v:
                continue
                
            if v.status == "PASS":
                lines.append(f"[PASS - {claim.claim_id}] {claim.text}")
            elif v.status == "FLAG":
                reasons = ", ".join(v.reason_codes)
                lines.append(f"[FLAG - {claim.claim_id}] {claim.text} *(Warning: {reasons})*")
            elif v.status == "REJECT":
                reasons = ", ".join(v.reason_codes)
                lines.append(f"~~[REJECTED/WITHHELD - {claim.claim_id}]~~ *(Reason: {reasons})*")

        if draft.missing_information:
            lines.append("\n### MISSING INFORMATION / PLACEHOLDERS")
            for m in draft.missing_information:
                lines.append(f"- {m}")

        return "\n".join(lines)
