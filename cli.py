"""
cli.py - Command-Line Interface Backend
Allows executing all workflows, pre-draft audits, and verification gates directly from the terminal.
Supports Multi-Jurisdiction: INDIA, UNITED STATES, UNITED KINGDOM, EUROPE (EU).
"""

import os
import sys
import argparse
import json

WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))
if WORKSPACE_DIR not in sys.path:
    sys.path.insert(0, WORKSPACE_DIR)

from core.pipeline_coordinator import PipelineCoordinator

SCENARIO_MAP = {
    # INDIA
    "theft_bns": (
        "bail_petition",
        "Draft bail petition under Section 303 BNS 2023",
        "In the Court of Judicial Magistrate First Class, Indore. Crime No. 204/2024. The accused Ramesh Kumar was arrested on 15 August 2024 from M.G. Road. It is alleged that the accused took possession of a mobile phone belonging to complainant Mohan Sharma without his consent. Accused has no criminal antecedents."
    ),
    "contract_ica": (
        "contract_case_review",
        "Review contract breach claim under Section 73 of Indian Contract Act 1872",
        "Supply Agreement dated 10 January 2023. Supplier failed to deliver 500 units of raw materials by the agreed deadline of 30 March 2023. Buyer suffered loss of Rs. 4,50,000 due to factory stoppage. Clause 14 specifies liquidated damages."
    ),
    "contradictory_dates": (
        "bail_petition",
        "Prepare bail petition for Vijay Singh",
        "Remand Application: The accused was arrested on 12 June 2024 at 10 PM. Police Diary Extract: The accused was arrested on 14 June 2024 near Railway Station. Complainant alleges loss of Rs. 50,000."
    ),
    "fake_section": (
        "rag_chat",
        "Is the accused liable under Section 999 of BNS 2023?",
        "The prosecution charges the accused under Section 999 of Bharatiya Nyaya Sanhita 2023 for aggravated misconduct."
    ),

    # UNITED STATES
    "us_theft_18usc": (
        "legal_research",
        "Analyze theft of public property under Section 641 of Title 18 U.S.C.",
        "Investigation indicates government contractor employee knowingly removed and sold federal laboratory equipment valued at $45,000 without authorization."
    ),
    "us_ucc_contract": (
        "contract_case_review",
        "Evaluate statute of frauds defense under UCC Article 2 Section 2-201",
        "Commercial contract for sale of industrial machinery for $75,000 was negotiated verbally without a signed writing. Buyer seeks enforcement."
    ),

    # UNITED KINGDOM
    "uk_theft_act": (
        "legal_research",
        "Analyze dishonest appropriation under Section 1 of the Theft Act 1968",
        "Defendant took bicycle parked outside train station believing the owner had abandoned it permanently."
    ),
    "uk_consumer_rights": (
        "contract_case_review",
        "Review quality terms under Section 9 of the Consumer Rights Act 2015",
        "Consumer purchased motor vehicle that suffered transmission failure within 14 days of purchase. Dealer denies warranty."
    ),

    # EUROPE (EU)
    "eu_gdpr": (
        "legal_research",
        "Examine lawfulness of processing under Article 5 and Article 6 of GDPR",
        "Company processed and shared user location logs with third-party advertising brokers without explicit consent."
    ),
    "eu_ai_act": (
        "contract_case_review",
        "Assess compliance under Article 5 of the EU AI Act",
        "Vendor proposes deploying real-time biometric and subliminal emotion-manipulating software in commercial workplaces."
    )
}

def main():
    parser = argparse.ArgumentParser(description="Multi-Jurisdiction Offline Legal Assistant Backend CLI")
    parser.add_argument("--workflow", choices=["bail_petition", "contract_case_review", "legal_research", "rag_chat"], default="bail_petition", help="Legal workflow")
    parser.add_argument("--query", type=str, help="Legal query or drafting task")
    parser.add_argument("--file", type=str, help="Path to input case PDF, TXT, or MD")
    parser.add_argument("--text", type=str, help="Inline raw text dossier")
    parser.add_argument("--scenario", choices=list(SCENARIO_MAP.keys()), help="Run pre-configured benchmark scenario")
    parser.add_argument("--json", action="store_true", help="Output full JSON result instead of formatted terminal summary")

    args = parser.parse_args()

    workflow = args.workflow
    query = args.query
    raw_text = args.text
    file_paths = [args.file] if args.file else None

    if args.scenario:
        wf, q, txt = SCENARIO_MAP[args.scenario]
        workflow = wf
        query = q
        raw_text = txt

    if not query:
        query = "Draft legal assessment under relevant statutory provisions"

    coordinator = PipelineCoordinator()
    result = coordinator.orchestrator.execute_workflow(
        workflow=workflow,
        query=query,
        document_paths=file_paths,
        raw_text_dossier=raw_text
    )

    if args.json:
        print(json.dumps(result.model_dump(), indent=2))
        return

    # Formatted terminal output
    print("\n" + "=" * 70)
    print(" MULTI-JURISDICTION AUDITED LEGAL RESULT")
    print("=" * 70)
    print(f"Workflow: {result.workflow}")
    print(f"Query:    {result.query_or_task}")
    print(f"RAM Used: {result.telemetry.ram_used_mb} MB (Budget: <= 3.5 GB)")
    print(f"Network:  {result.telemetry.network_status} (0 Outbound Calls)")

    if result.contradictions:
        print("\n[!] CONFLICTS DETECTED ACROSS DOSSIER:")
        for c in result.contradictions:
            print(f"  - {c.topic}: '{c.statement_a}' vs '{c.statement_b}'")

    if result.pre_draft_audit.unknown_facts:
        print("\n[?] PRE-DRAFT MISSING INFORMATION / PLACEHOLDERS:")
        for u in result.pre_draft_audit.unknown_facts:
            print(f"  - {u}")

    print("\n[✓] CLAIM-LEVEL AUDIT VERDICTS:")
    if not result.claims:
        print("  - [ABSTAIN / NOT_VERIFIED]: Insufficient evidence to support claim.")
    else:
        for c in result.claims:
            v = result.structured_draft.verdicts.get(c.claim_id)
            status = v.status if v else "FLAG"
            reasons = f" ({', '.join(v.reason_codes)})" if (v and v.reason_codes and v.status != "PASS") else ""
            print(f"  [{status}] {c.claim_id}: {c.text}{reasons}")

    print("\n" + "-" * 70)
    print("FINAL AUDITED OUTPUT:")
    print("-" * 70)
    print(result.final_audited_text)
    print("=" * 70 + "\n")

if __name__ == "__main__":
    main()
