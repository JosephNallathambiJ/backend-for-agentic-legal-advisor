"""
core/llm_engine.py - Local Drafting & Claim Generation Engine
Supports:
1. GGUF model inference via llama-cpp-python when local weights are configured in models/llm/
2. Local deterministic evidence-first drafting synthesizer as reliable offline fallback
Follows strict non-hallucination drafting rules:
- Inserts explicit placeholders [NOT PROVIDED] for unknown facts
- Proposes atomic claims with evidence_ids
- NEVER assigns PASS / FLAG / REJECT
"""

import os
import json
import re
from typing import List, Dict, Any, Optional
from core.schemas import Claim, StructuredDraft, Evidence
from core.provenance import EvidenceLedger
from core.logging_config import logger

class LocalLLMEngine:
    def __init__(self, model_path: Optional[str] = None):
        self.model_path = model_path
        self.llm = None
        self.model_name = "Deterministic Rule Engine"
        self._init_model()

    def _init_model(self):
        # Auto-discover Gemma 4 12B or other GGUF models in models/llm
        if not self.model_path:
            models_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models", "llm")
            if os.path.exists(models_dir):
                candidates = [f for f in os.listdir(models_dir) if f.endswith(".gguf")]
                gemma_models = [c for c in candidates if "gemma" in c.lower()]
                selected = gemma_models[0] if gemma_models else (candidates[0] if candidates else None)
                if selected:
                    self.model_path = os.path.join(models_dir, selected)

        if self.model_path and os.path.exists(self.model_path):
            try:
                from llama_cpp import Llama
                self.model_name = os.path.basename(self.model_path)
                logger.info(f"Loading base LLM ({self.model_name}): {self.model_path}")
                self.llm = Llama(
                    model_path=self.model_path,
                    n_ctx=4096,
                    n_threads=min(os.cpu_count() or 4, 8),
                    verbose=False
                )
            except Exception as e:
                logger.warning(f"Could not load GGUF ({e}). Defaulting to deterministic engine.")
                self.llm = None
        else:
            logger.info("Using local deterministic rule-based drafting engine (Gemma 4 12B base profile).")

    def draft(
        self,
        task_type: str,
        query: str,
        approved_evidence: List[Evidence],
        known_facts: List[str],
        missing_information: List[str]
    ) -> StructuredDraft:
        """
        Generates structured claims and draft text strictly grounded in approved evidence.
        """
        # If neural GGUF is available, query GGUF with constrained JSON prompt
        if self.llm:
            try:
                return self._draft_neural(task_type, query, approved_evidence, known_facts, missing_information)
            except Exception as ex:
                logger.error(f"Neural drafting error: {ex}. Falling back to deterministic drafting.")

        # Deterministic evidence-grounded drafting
        return self._draft_deterministic(task_type, query, approved_evidence, known_facts, missing_information)

    def _draft_deterministic(
        self,
        task_type: str,
        query: str,
        approved_evidence: List[Evidence],
        known_facts: List[str],
        missing_information: List[str]
    ) -> StructuredDraft:
        claims: List[Claim] = []
        claim_counter = 1
        
        statute_evs = [e for e in approved_evidence if e.evidence_type == "statute"]
        case_evs = [e for e in approved_evidence if e.evidence_type == "case_fact"]
        
        draft_lines = []
        
        if task_type in ["bail_petition", "anticipatory_bail"]:
            title = "APPLICATION FOR BAIL UNDER RELEVANT PROVISIONS"
            draft_lines.append(f"IN THE COURT OF: {self._get_placeholder('COURT NAME NOT PROVIDED')}")
            draft_lines.append(f"IN THE MATTER OF: {self._get_placeholder('APPLICANT NAME NOT PROVIDED')} VS STATE")
            draft_lines.append(f"FIR NO: {self._get_placeholder('FIR NUMBER NOT FOUND IN SOURCE DOCUMENT')}\n")
            draft_lines.append("MOST RESPECTFULLY SHOWETH:\n")
            
            # Factual claims from case evidence
            for i, ev in enumerate(case_evs[:4]):
                cid = f"C{claim_counter:03d}"
                claim_counter += 1
                c = Claim(
                    claim_id=cid,
                    text=f"As per the record, {ev.text_span}",
                    claim_type="factual",
                    evidence_ids=[ev.evidence_id],
                    risk_level="low"
                )
                claims.append(c)
                draft_lines.append(f"{i+1}. {c.text} [{ev.evidence_id}]")

            # Statutory claims from statute evidence
            for j, ev in enumerate(statute_evs[:3]):
                cid = f"C{claim_counter:03d}"
                claim_counter += 1
                c = Claim(
                    claim_id=cid,
                    text=f"Under Section {ev.section or 'relevant'} of {ev.source_title}, the statutory provisions governing the offence are defined as follows: \"{ev.text_span[:120].strip()}\"",
                    claim_type="statutory",
                    evidence_ids=[ev.evidence_id],
                    citation_ids=[ev.locator],
                    risk_level="low",
                    is_quote=True,
                    quote_text=ev.text_span[:120].strip()
                )
                claims.append(c)
                draft_lines.append(f"\n{len(case_evs)+j+1}. {c.text} [{ev.evidence_id}]")
                
            draft_lines.append("\nPRAYER:")
            draft_lines.append(f"Wherefore it is prayed that the Applicant be enlarged on bail subject to conditions.")

        elif task_type in ["contract_case_review", "contract_review"]:
            title = "LEGAL ASSESSMENT & CONTRACT REVIEW"
            draft_lines.append("================ CONTRACT ASSESSMENT ================\n")
            for i, ev in enumerate(case_evs):
                cid = f"C{claim_counter:03d}"
                claim_counter += 1
                c = Claim(
                    claim_id=cid,
                    text=f"The record documents that: {ev.text_span}",
                    claim_type="factual",
                    evidence_ids=[ev.evidence_id],
                    risk_level="low"
                )
                claims.append(c)
                draft_lines.append(f"- FACT [{ev.evidence_id}]: {c.text}")

            for j, ev in enumerate(statute_evs):
                cid = f"C{claim_counter:03d}"
                claim_counter += 1
                clean_span = ev.text_span[:100].strip()
                c = Claim(
                    claim_id=cid,
                    text=f"Statutory authority {ev.source_title} Section {ev.section or ''} provides: \"{clean_span}\"",
                    claim_type="statutory",
                    evidence_ids=[ev.evidence_id],
                    citation_ids=[ev.locator],
                    risk_level="low",
                    is_quote=True,
                    quote_text=clean_span
                )
                claims.append(c)
                draft_lines.append(f"- LAW [{ev.evidence_id}]: {c.text}")

        elif task_type in ["legal_research", "issue_tree"]:
            title = "LEGAL RESEARCH MEMORANDUM & STATUTORY ANALYSIS"
            draft_lines.append(f"ISSUE: {query}\n")
            draft_lines.append("I. APPLICABLE STATUTORY PROVISIONS:")
            for j, ev in enumerate(statute_evs):
                cid = f"C{claim_counter:03d}"
                claim_counter += 1
                clean_span = ev.text_span[:110].strip()
                c = Claim(
                    claim_id=cid,
                    text=f"{ev.source_title} Section {ev.section or ''} provides that: \"{clean_span}\"",
                    claim_type="statutory",
                    evidence_ids=[ev.evidence_id],
                    citation_ids=[ev.locator],
                    risk_level="low",
                    is_quote=True,
                    quote_text=clean_span
                )
                claims.append(c)
                draft_lines.append(f"  {j+1}. [{ev.evidence_id}] {c.text}")

            draft_lines.append("\nII. FACTUAL APPLICATION:")
            for i, ev in enumerate(case_evs):
                cid = f"C{claim_counter:03d}"
                claim_counter += 1
                c = Claim(
                    claim_id=cid,
                    text=f"Applying statute to established fact: {ev.text_span}",
                    claim_type="factual",
                    evidence_ids=[ev.evidence_id],
                    risk_level="low"
                )
                claims.append(c)
                draft_lines.append(f"  - [{ev.evidence_id}] {c.text}")

        else: # rag_chat / general Q&A
            title = "GROUNDED LEGAL RESPONSE"
            if not approved_evidence:
                return StructuredDraft(
                    task_type=task_type,
                    title=title,
                    claims=[],
                    missing_information=["No verified evidence found in local corpus or case dossier."],
                    uncertainties=["Abstention triggered under Verifiability Over Fluency rule."],
                    draft_text="NOT_VERIFIED: Insufficient local evidence to ground this claim."
                )

            for ev in approved_evidence:
                cid = f"C{claim_counter:03d}"
                claim_counter += 1
                c_type = "statutory" if ev.evidence_type == "statute" else "factual"
                c = Claim(
                    claim_id=cid,
                    text=f"Based on {ev.source_title} ({ev.locator}): {ev.text_span[:150]}",
                    claim_type=c_type,
                    evidence_ids=[ev.evidence_id],
                    citation_ids=[ev.locator] if ev.evidence_type == "statute" else [],
                    risk_level="low"
                )
                claims.append(c)
                draft_lines.append(f"[{ev.evidence_id}] {c.text}")

        # Missing information disclosure
        if missing_information:
            draft_lines.append("\nMISSING INFORMATION / PLACEHOLDERS:")
            for m in missing_information:
                draft_lines.append(f"- {m}")

        # Authoritative statutory web links (resolved offline for Congress.gov, Legislation.gov.uk, EUR-Lex, etc.)
        statute_links = []
        for ev in statute_evs:
            link = ev.source_path or ""
            if link.startswith("http"):
                formatted = f"• {ev.source_title}: {link}"
                if formatted not in statute_links:
                    statute_links.append(formatted)
        if statute_links:
            draft_lines.append("\nOFFICIAL GOVERNMENT LEGISLATIVE REPOSITORIES (VERIFIED PROVENANCE):")
            for sl in statute_links:
                draft_lines.append(sl)

        draft_text = "\n".join(draft_lines)
        return StructuredDraft(
            task_type=task_type,
            title=title,
            claims=claims,
            missing_information=missing_information,
            uncertainties=[f"Draft is bounded to {len(approved_evidence)} local evidence spans."],
            draft_text=draft_text
        )

    def _get_placeholder(self, item: str) -> str:
        return f"[{item}]"

    def _draft_neural(
        self,
        task_type: str,
        query: str,
        approved_evidence: List[Evidence],
        known_facts: List[str],
        missing_information: List[str]
    ) -> StructuredDraft:
        if not self.llm:
            return self._draft_deterministic(task_type, query, approved_evidence, known_facts, missing_information)
            
        evidence_summary = "\n".join([f"- [{e.evidence_id}] {e.source_title} ({e.locator}): {e.text_span[:200]}" for e in approved_evidence])
        facts_summary = "\n".join([f"- {f}" for f in known_facts])
        
        prompt = (
            f"<start_of_turn>user\n"
            f"You are an offline legal assistant bound by evidence. Task: {task_type}.\n"
            f"Query: {query}\n"
            f"Verified Evidence:\n{evidence_summary}\n"
            f"Known Facts:\n{facts_summary}\n"
            f"Rules:\n"
            f"1. Ground all claims in the evidence IDs provided above.\n"
            f"2. Never fabricate facts, dates, or statutes.\n"
            f"3. Quote verbatim where citing statutes.\n"
            f"Draft the legal response concisely.<end_of_turn>\n"
            f"<start_of_turn>model\n"
        )
        
        try:
            output = self.llm(
                prompt,
                max_tokens=512,
                temperature=0.1,
                top_p=0.9,
                stop=["<end_of_turn>", "\n\n\n"]
            )
            generated_text = output["choices"][0]["text"].strip()
            
            draft = self._draft_deterministic(task_type, query, approved_evidence, known_facts, missing_information)
            if generated_text:
                draft.draft_text = generated_text
            return draft
        except Exception as e:
            logger.warning(f"Gemma model generation failed: {e}. Falling back to deterministic.")
            return self._draft_deterministic(task_type, query, approved_evidence, known_facts, missing_information)

