"""
cli.py - Command-Line Interface Backend
Allows executing all workflows, pre-draft audits, and verification gates directly from the terminal.
Supports Multi-Jurisdiction: INDIA, UNITED STATES, UNITED KINGDOM, EUROPE (EU).
"""

import os
import sys
import argparse
import json
import re

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
    ),

    # NORTHERN & EASTERN EUROPE
    "belarus_const": (
        "legal_research",
        "Evaluate personal liberty under Article 25 of Belarus Constitution",
        "Detained citizen challenges unlawful multi-day detention without judicial order in Minsk (+375)."
    ),
    "bulgaria_const": (
        "legal_research",
        "Evaluate presumption of innocence under Article 31 of Bulgarian Constitution",
        "Defendant in Sofia (+359) was subjected to coercive confession prior to presentation before a magistrate."
    ),
    "poland_const": (
        "legal_research",
        "Analyze penal legality principle under Article 42 of Polish Constitution",
        "Petitioner in Warsaw (+48) was charged under retroactive penal regulation not in force at time of occurrence."
    ),
    "sweden_const": (
        "legal_research",
        "Review fair trial rights under Chapter 2 Section 11 of Swedish Constitution",
        "Appellant in Stockholm (+46) asserts closed-door proceeding breached constitutional public trial mandates."
    ),
    "ukraine_const": (
        "legal_research",
        "Review rule of law and constitutional supremacy under Article 8 of Ukrainian Constitution",
        "Petitioner in Kyiv (+380) challenges subordinate administrative regulation contradicting supreme constitutional force."
    ),
    "us_constitution": (
        "legal_research",
        "Assess Fourth Amendment protections under Constitution of the United States",
        "Federal agents conducted warrantless search and seizure of private records without probable cause or warrant."
    )
}

def main():
    parser = argparse.ArgumentParser(description="Multi-Jurisdiction Offline Legal Assistant Backend CLI")
    parser.add_argument("--workflow", choices=["bail_petition", "contract_case_review", "legal_research", "rag_chat"], default="bail_petition", help="Legal workflow")
    parser.add_argument("--query", type=str, help="Legal query or drafting task")
    parser.add_argument("--file", type=str, help="Path to input case PDF, TXT, or MD")
    parser.add_argument("--text", type=str, help="Inline raw text dossier")
    parser.add_argument("--scenario", choices=list(SCENARIO_MAP.keys()), help="Run pre-configured benchmark scenario")
    parser.add_argument("--portals", action="store_true", help="Display official court and legislation portals by country")
    parser.add_argument("--link", type=str, help="Resolve official government portal URL for any statute or citation (US Congress.gov, UK Legislation.gov.uk, EUR-Lex, etc.)")
    parser.add_argument("--json", action="store_true", help="Output full JSON result instead of formatted terminal summary")

    args = parser.parse_args()

    if args.link:
        from core.statute_web_linker import statute_linker
        from core.legal_router import LegalRouter
        router = LegalRouter()
        jurisdiction, act_ids = router.route_query(args.link)
        act_id = act_ids[0] if act_ids else "US_CONST_1787"
        sec_match = re.search(r"\b(?:section|sec\.?|s\.|article|art\.?)\s*([0-9]+[A-Z0-9\-_.:]*)", args.link, re.IGNORECASE)
        sec_num = sec_match.group(1) if sec_match else None
        info = statute_linker.resolve_statute_link(act_id, sec_num)
        if args.json:
            print(json.dumps(info, indent=2))
        else:
            print("\n" + "=" * 75)
            print("OFFICIAL GOVERNMENT LEGISLATIVE REPOSITORY RESOLVER (AIR-GAPPED)")
            print("=" * 75)
            print(f"Query / Citation:     {args.link}")
            print(f"Jurisdiction:         {info['jurisdiction']}")
            print(f"Statutory Act:        {info['act_title']}")
            if info['section_number']:
                print(f"Section / Article:    {info['section_number']}")
            print(f"Authoritative Portal: {info['portal_name']}")
            print(f"Managing Authority:   {info['managing_authority']}")
            print(f"Official Act URL:     {info['official_act_url']}")
            print(f"Official Section URL: {info['official_section_url']}")
            print("=" * 75 + "\n")
        return

    if args.portals:
        portals_csv = os.path.join(WORKSPACE_DIR, "data", "csv", "court_portals_registry.csv")
        if os.path.exists(portals_csv):
            import pandas as pd
            df = pd.read_csv(portals_csv)
            if args.json:
                print(json.dumps(df.to_dict(orient="records"), indent=2))
            else:
                print("\n" + "=" * 95)
                print(f"{'COUNTRY':<18} {'DIAL':<6} {'LEGISLATION PORTAL':<32} {'COURT PORTAL'}")
                print("=" * 95)
                for _, r in df.iterrows():
                    print(f"{r['country']:<18} {r['dial_code']:<6} {str(r['legislation_portal_url']):<32} {str(r['supreme_court_portal_url'])}")
                print("=" * 95 + "\n")
        else:
            print("Portals registry not found.")
        return

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
