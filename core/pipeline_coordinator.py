"""
core/pipeline_coordinator.py - Primary Workflow Coordinator
Coordinates the 4 key legal workflows:
1. Contract / Case Review
2. Legal Drafting (Bail, Legal Notice, Reply, etc.)
3. Legal Research (Issue tree, statutory analysis)
4. Grounded RAG Chat
"""

from typing import List, Optional, Dict, Any
from core.agent_orchestrator import AgentOrchestrator
from core.provenance import EvidenceLedger
from core.schemas import PipelineResult

class PipelineCoordinator:
    def __init__(self):
        # Dedicated orchestrator instance per session
        self.orchestrator = AgentOrchestrator()

    def reset_session(self):
        """Clears memory and starts clean session isolation."""
        self.orchestrator = AgentOrchestrator()

    def run_contract_case_review(
        self,
        query: str = "Review uploaded contract and identify obligations and risks",
        document_paths: Optional[List[str]] = None,
        raw_text: Optional[str] = None
    ) -> PipelineResult:
        return self.orchestrator.execute_workflow(
            workflow="contract_case_review",
            query=query,
            document_paths=document_paths,
            raw_text_dossier=raw_text
        )

    def run_legal_drafting(
        self,
        draft_type: str = "bail_petition",
        query: str = "Draft bail petition under relevant statutory provisions",
        document_paths: Optional[List[str]] = None,
        raw_text: Optional[str] = None
    ) -> PipelineResult:
        return self.orchestrator.execute_workflow(
            workflow=draft_type,
            query=query,
            document_paths=document_paths,
            raw_text_dossier=raw_text
        )

    def run_legal_research(
        self,
        issue_query: str,
        document_paths: Optional[List[str]] = None,
        raw_text: Optional[str] = None
    ) -> PipelineResult:
        return self.orchestrator.execute_workflow(
            workflow="legal_research",
            query=issue_query,
            document_paths=document_paths,
            raw_text_dossier=raw_text
        )

    def run_rag_chat(
        self,
        question: str,
        document_paths: Optional[List[str]] = None,
        raw_text: Optional[str] = None
    ) -> PipelineResult:
        return self.orchestrator.execute_workflow(
            workflow="rag_chat",
            query=question,
            document_paths=document_paths,
            raw_text_dossier=raw_text
        )
