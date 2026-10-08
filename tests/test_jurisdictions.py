"""
tests/test_jurisdictions.py - Multi-Jurisdiction Verification Tests
Validates statutory retrieval, citation validation, and exact quote checks across:
- INDIA (BNS 2023, Contract Act 1872)
- UNITED STATES (Title 18 U.S.C., UCC Article 2)
- UNITED KINGDOM (Theft Act 1968, Contracts Act 1999)
- EUROPE / EU (GDPR Regulation 2016/679, EU AI Act 2024/1689)
"""

import pytest
from core.provenance import EvidenceLedger
from core.local_legal_retriever import LocalLegalRetriever
from core.verifier import DeterministicVerifier
from core.legal_router import LegalRouter
from core.schemas import Claim

def test_jurisdiction_us_title18():
    ledger = EvidenceLedger()
    retriever = LocalLegalRetriever(ledger)
    verifier = DeterministicVerifier(ledger)

    ev = retriever.lookup_section("US_TITLE_18", "641")
    assert ev is not None
    assert ev.jurisdiction == "US"
    assert "embezzles" in ev.text_span.lower() or "steals" in ev.text_span.lower()

    claim = Claim(
        claim_id="C_US_01",
        text="Under Section 641 of Title 18 U.S.C., stealing public property is prohibited.",
        claim_type="statutory",
        evidence_ids=[ev.evidence_id],
        citation_ids=[ev.locator]
    )
    verdict = verifier.verify_claim(claim)
    assert verdict.status == "PASS"

def test_jurisdiction_us_ucc_sales():
    ledger = EvidenceLedger()
    retriever = LocalLegalRetriever(ledger)
    verifier = DeterministicVerifier(ledger)

    ev = retriever.lookup_section("US_UCC_ART_2", "2-201")
    assert ev is not None
    assert ev.jurisdiction == "US"
    assert "statute of frauds" in ev.text_span.lower() or "$500" in ev.text_span

    claim = Claim(
        claim_id="C_US_02",
        text="Section 2-201 of UCC Article 2 establishes formal writing requirements for contracts of sale.",
        claim_type="statutory",
        evidence_ids=[ev.evidence_id],
        citation_ids=[ev.locator]
    )
    verdict = verifier.verify_claim(claim)
    assert verdict.status == "PASS"

def test_jurisdiction_uk_theft_act():
    ledger = EvidenceLedger()
    retriever = LocalLegalRetriever(ledger)
    verifier = DeterministicVerifier(ledger)

    ev = retriever.lookup_section("UK_THEFT_1968", "1")
    assert ev is not None
    assert ev.jurisdiction == "UK"
    assert "permanently depriving" in ev.text_span.lower()

    claim = Claim(
        claim_id="C_UK_01",
        text="Section 1 of the Theft Act 1968 defines theft as dishonestly appropriating property belonging to another.",
        claim_type="statutory",
        evidence_ids=[ev.evidence_id],
        citation_ids=[ev.locator]
    )
    verdict = verifier.verify_claim(claim)
    assert verdict.status == "PASS"

def test_jurisdiction_eu_gdpr():
    ledger = EvidenceLedger()
    retriever = LocalLegalRetriever(ledger)
    verifier = DeterministicVerifier(ledger)

    ev = retriever.lookup_section("EU_GDPR_2016", "5")
    assert ev is not None
    assert ev.jurisdiction == "EU"
    assert "lawfulness" in ev.text_span.lower()

    claim = Claim(
        claim_id="C_EU_01",
        text="Article 5 of GDPR mandates principles of lawfulness, fairness, and transparency in personal data processing.",
        claim_type="statutory",
        evidence_ids=[ev.evidence_id],
        citation_ids=[ev.locator]
    )
    verdict = verifier.verify_claim(claim)
    assert verdict.status == "PASS"

def test_jurisdiction_eu_ai_act():
    ledger = EvidenceLedger()
    retriever = LocalLegalRetriever(ledger)
    verifier = DeterministicVerifier(ledger)

    ev = retriever.lookup_section("EU_AI_ACT_2024", "5")
    assert ev is not None
    assert ev.jurisdiction == "EU"
    assert "prohibited" in ev.text_span.lower()

    claim = Claim(
        claim_id="C_EU_02",
        text="Article 5 of EU AI Act bans manipulative subliminal AI techniques and social scoring systems.",
        claim_type="statutory",
        evidence_ids=[ev.evidence_id],
        citation_ids=[ev.locator]
    )
    verdict = verifier.verify_claim(claim)
    assert verdict.status == "PASS"

def test_jurisdiction_router_auto_detection():
    router = LegalRouter()
    assert router.detect_jurisdiction("What are requirements under GDPR Article 5?") == "EU"
    assert router.detect_jurisdiction("Check Wire Fraud under Title 18 USC Section 1343") == "US"
    assert router.detect_jurisdiction("Theft under Theft Act 1968 Section 1") == "UK"
    assert router.detect_jurisdiction("Bail application under Section 303 BNS 2023") == "INDIA"
    assert router.detect_jurisdiction("Detention in Minsk under Belarus Constitution (+375)") == "BELARUS"
    assert router.detect_jurisdiction("Presumption of innocence in Sofia (+359) under Bulgarian Constitution") == "BULGARIA"
    assert router.detect_jurisdiction("Legality principle under Polish Constitution in Warsaw (+48)") == "POLAND"
    assert router.detect_jurisdiction("Public trial rights under Swedish Constitution (+46)") == "SWEDEN"
    assert router.detect_jurisdiction("Constitutional supremacy in Kyiv (+380) under Ukrainian Constitution") == "UKRAINE"

def test_jurisdiction_us_constitution():
    ledger = EvidenceLedger()
    retriever = LocalLegalRetriever(ledger)
    verifier = DeterministicVerifier(ledger)

    ev = retriever.lookup_section("US_CONST_1787", "Amend4")
    assert ev is not None
    assert ev.jurisdiction == "US"
    assert "unreasonable searches" in ev.text_span.lower()

    claim = Claim(
        claim_id="C_US_CONST_01",
        text="The Fourth Amendment protects the right of people against unreasonable searches and seizures.",
        claim_type="statutory",
        evidence_ids=[ev.evidence_id],
        citation_ids=[ev.locator]
    )
    verdict = verifier.verify_claim(claim)
    assert verdict.status == "PASS"

def test_jurisdiction_belarus_constitution():
    ledger = EvidenceLedger()
    retriever = LocalLegalRetriever(ledger)
    verifier = DeterministicVerifier(ledger)

    ev = retriever.lookup_section("BY_CONST_1994", "25")
    assert ev is not None
    assert ev.jurisdiction == "BELARUS"
    assert "personal freedom" in ev.text_span.lower()

    claim = Claim(
        claim_id="C_BY_01",
        text="Article 25 of Belarus Constitution guarantees personal freedom and prohibits torture or cruel treatment.",
        claim_type="statutory",
        evidence_ids=[ev.evidence_id],
        citation_ids=[ev.locator]
    )
    verdict = verifier.verify_claim(claim)
    assert verdict.status == "PASS"

def test_jurisdiction_bulgaria_constitution():
    ledger = EvidenceLedger()
    retriever = LocalLegalRetriever(ledger)
    verifier = DeterministicVerifier(ledger)

    ev = retriever.lookup_section("BG_CONST_1991", "31")
    assert ev is not None
    assert ev.jurisdiction == "BULGARIA"
    assert "presumed innocent" in ev.text_span.lower() or "innocent until proven guilty" in ev.text_span.lower()

    claim = Claim(
        claim_id="C_BG_01",
        text="Under Article 31 of Bulgarian Constitution, accused persons are considered innocent until proven guilty.",
        claim_type="statutory",
        evidence_ids=[ev.evidence_id],
        citation_ids=[ev.locator]
    )
    verdict = verifier.verify_claim(claim)
    assert verdict.status == "PASS"

def test_jurisdiction_poland_constitution():
    ledger = EvidenceLedger()
    retriever = LocalLegalRetriever(ledger)
    verifier = DeterministicVerifier(ledger)

    ev = retriever.lookup_section("PL_CONST_1997", "42")
    assert ev is not None
    assert ev.jurisdiction == "POLAND"
    assert "criminally responsible" in ev.text_span.lower()

    claim = Claim(
        claim_id="C_PL_01",
        text="Article 42 of Polish Constitution codifies penal legality and presumption of innocence.",
        claim_type="statutory",
        evidence_ids=[ev.evidence_id],
        citation_ids=[ev.locator]
    )
    verdict = verifier.verify_claim(claim)
    assert verdict.status == "PASS"

def test_jurisdiction_sweden_constitution():
    ledger = EvidenceLedger()
    retriever = LocalLegalRetriever(ledger)
    verifier = DeterministicVerifier(ledger)

    ev = retriever.lookup_section("SE_CONST_1974", "2:11")
    assert ev is not None
    assert ev.jurisdiction == "SWEDEN"
    assert "fairly and within a reasonable time" in ev.text_span.lower()

    claim = Claim(
        claim_id="C_SE_01",
        text="Under Chapter 2 Section 11 of Swedish Constitution, judicial hearings must be public and conducted fairly.",
        claim_type="statutory",
        evidence_ids=[ev.evidence_id],
        citation_ids=[ev.locator]
    )
    verdict = verifier.verify_claim(claim)
    assert verdict.status == "PASS"

def test_jurisdiction_ukraine_constitution():
    ledger = EvidenceLedger()
    retriever = LocalLegalRetriever(ledger)
    verifier = DeterministicVerifier(ledger)

    ev = retriever.lookup_section("UA_CONST_1996", "8")
    assert ev is not None
    assert ev.jurisdiction == "UKRAINE"
    assert "highest legal force" in ev.text_span.lower()

    claim = Claim(
        claim_id="C_UA_01",
        text="Article 8 of Ukrainian Constitution establishes the highest legal force of the constitution and the rule of law.",
        claim_type="statutory",
        evidence_ids=[ev.evidence_id],
        citation_ids=[ev.locator]
    )
    verdict = verifier.verify_claim(claim)
    assert verdict.status == "PASS"

def test_court_portals_registry():
    import os
    import pandas as pd
    from core.legal_router import WORKSPACE_DIR

    portals_csv = os.path.join(WORKSPACE_DIR, "data", "csv", "court_portals_registry.csv")
    assert os.path.exists(portals_csv)
    df = pd.read_csv(portals_csv)
    assert len(df) >= 22

    # Check that required Northern and Eastern European countries are present with dial codes
    target_countries = [
        "Belarus", "Bulgaria", "Czech Republic", "Denmark", "Estonia",
        "Finland", "Hungary", "Iceland", "Ireland", "Latvia", "Lithuania",
        "Norway", "Poland", "Romania", "Russia", "Slovakia", "Sweden", "Ukraine", "United States"
    ]
    for c in target_countries:
        matched = df[df["country"] == c]
        assert len(matched) == 1, f"Missing portal entry for {c}"
        assert matched["legislation_portal_url"].values[0].startswith("http")
        assert matched["supreme_court_portal_url"].values[0].startswith("http")

def test_jurisdiction_us_civil_rights_and_sherman():
    ledger = EvidenceLedger()
    retriever = LocalLegalRetriever(ledger)
    verifier = DeterministicVerifier(ledger)

    ev_cra = retriever.lookup_section("US_CIVIL_RIGHTS_1964", "703")
    assert ev_cra is not None
    assert ev_cra.jurisdiction == "US"
    assert "unlawful employment practice" in ev_cra.text_span.lower()

    claim = Claim(
        claim_id="C_US_CRA_01",
        text="Section 703 of Civil Rights Act of 1964 prohibits discriminatory employment practices based on race, color, or religion.",
        claim_type="statutory",
        evidence_ids=[ev_cra.evidence_id],
        citation_ids=[ev_cra.locator]
    )
    verdict = verifier.verify_claim(claim)
    assert verdict.status == "PASS"

    ev_sherman = retriever.lookup_section("US_SHERMAN_1890", "1")
    assert ev_sherman is not None
    assert "restraint of trade" in ev_sherman.text_span.lower()

def test_jurisdiction_uk_fraud_and_human_rights():
    ledger = EvidenceLedger()
    retriever = LocalLegalRetriever(ledger)
    verifier = DeterministicVerifier(ledger)

    ev_fraud = retriever.lookup_section("UK_FRAUD_2006", "2")
    assert ev_fraud is not None
    assert ev_fraud.jurisdiction == "UK"
    assert "false representation" in ev_fraud.text_span.lower()

    claim = Claim(
        claim_id="C_UK_FRAUD_01",
        text="Section 2 of Fraud Act 2006 defines fraud by false representation made dishonestly.",
        claim_type="statutory",
        evidence_ids=[ev_fraud.evidence_id],
        citation_ids=[ev_fraud.locator]
    )
    verdict = verifier.verify_claim(claim)
    assert verdict.status == "PASS"

def test_jurisdiction_eu_dsa_and_tfeu():
    ledger = EvidenceLedger()
    retriever = LocalLegalRetriever(ledger)
    verifier = DeterministicVerifier(ledger)

    ev_dsa = retriever.lookup_section("EU_DSA_2022", "6")
    assert ev_dsa is not None
    assert ev_dsa.jurisdiction == "EU"
    assert "liable" in ev_dsa.text_span.lower() or "storage" in ev_dsa.text_span.lower()

    ev_tfeu = retriever.lookup_section("EU_TFEU_2012", "101")
    assert ev_tfeu is not None
    assert "incompatible with the internal market" in ev_tfeu.text_span.lower()

def test_jurisdiction_us_bankruptcy_and_patents():
    ledger = EvidenceLedger()
    retriever = LocalLegalRetriever(ledger)
    verifier = DeterministicVerifier(ledger)

    ev_bank = retriever.lookup_section("US_BANKRUPTCY_TITLE_11", "362")
    assert ev_bank is not None
    assert ev_bank.jurisdiction == "US"
    assert "stay" in ev_bank.text_span.lower()

    claim = Claim(
        claim_id="C_US_BANK_01",
        text="Section 362 of Title 11 Bankruptcy Code operates as an automatic stay against debtor proceedings.",
        claim_type="statutory",
        evidence_ids=[ev_bank.evidence_id],
        citation_ids=[ev_bank.locator]
    )
    verdict = verifier.verify_claim(claim)
    assert verdict.status == "PASS"

    ev_pat = retriever.lookup_section("US_PATENT_TITLE_35", "101")
    assert ev_pat is not None
    assert "inventions patentable" in ev_pat.text_span.lower() or "patent" in ev_pat.text_span.lower()

def test_jurisdiction_uk_sale_of_goods_and_bribery():
    ledger = EvidenceLedger()
    retriever = LocalLegalRetriever(ledger)
    verifier = DeterministicVerifier(ledger)

    ev_sga = retriever.lookup_section("UK_SALE_OF_GOODS_1979", "14")
    assert ev_sga is not None
    assert ev_sga.jurisdiction == "UK"
    assert "satisfactory quality" in ev_sga.text_span.lower()

    claim = Claim(
        claim_id="C_UK_SGA_01",
        text="Section 14 of Sale of Goods Act 1979 implies a term that goods supplied are of satisfactory quality.",
        claim_type="statutory",
        evidence_ids=[ev_sga.evidence_id],
        citation_ids=[ev_sga.locator]
    )
    verdict = verifier.verify_claim(claim)
    assert verdict.status == "PASS"

    ev_bribery = retriever.lookup_section("UK_BRIBERY_2010", "1")
    assert ev_bribery is not None
    assert "bribing" in ev_bribery.text_span.lower() or "advantage" in ev_bribery.text_span.lower()

def test_jurisdiction_eu_mica_and_teu():
    ledger = EvidenceLedger()
    retriever = LocalLegalRetriever(ledger)
    verifier = DeterministicVerifier(ledger)

    ev_mica = retriever.lookup_section("EU_MICA_2023", "3")
    assert ev_mica is not None
    assert ev_mica.jurisdiction == "EU"
    assert "crypto-asset" in ev_mica.text_span.lower()

    claim = Claim(
        claim_id="C_EU_MICA_01",
        text="Article 3 of Regulation (EU) 2023/1114 defines crypto-asset as a digital representation of value or rights.",
        claim_type="statutory",
        evidence_ids=[ev_mica.evidence_id],
        citation_ids=[ev_mica.locator]
    )
    verdict = verifier.verify_claim(claim)
    assert verdict.status == "PASS"

    ev_teu = retriever.lookup_section("EU_TEU_2016", "2")
    assert ev_teu is not None
    assert "rule of law" in ev_teu.text_span.lower()

def test_all_csv_files_filled_and_consistent():
    import os
    import pandas as pd
    from core.legal_router import WORKSPACE_DIR

    csv_dir = os.path.join(WORKSPACE_DIR, "data", "csv")
    csv_files = {
        "all_jurisdictions_acts.csv": 980,
        "court_portals_registry.csv": 22,
        "northern_eastern_europe_constitutions.csv": 18,
        "us_federal_statutes.csv": 30,
        "uk_statutes.csv": 25,
        "eu_regulations.csv": 25,
        "india_central_acts.csv": 876
    }

    for fname, min_rows in csv_files.items():
        fpath = os.path.join(csv_dir, fname)
        assert os.path.exists(fpath), f"Missing CSV: {fname}"
        df = pd.read_csv(fpath)
        assert len(df) >= min_rows, f"CSV {fname} has only {len(df)} rows, expected >= {min_rows}"
        assert not df.empty, f"CSV {fname} is empty"
        assert df.isnull().sum().sum() == 0, f"CSV {fname} contains null values: {df.isnull().sum().to_dict()}"
        if "sha256" in df.columns:
            for val in df["sha256"]:
                assert isinstance(val, str) and len(val) == 64, f"Invalid SHA-256 in {fname}"

def test_statute_web_linker_offline_resolution():
    from core.statute_web_linker import statute_linker

    # US resolution (Congress.gov / US Code)
    us_info = statute_linker.resolve_statute_link("US_TITLE_18", "641")
    assert "uscode.house.gov" in us_info["official_section_url"]
    assert us_info["jurisdiction"] == "US"
    assert us_info["is_airgapped_link"] is True

    # UK resolution (Legislation.gov.uk deep link)
    uk_info = statute_linker.resolve_statute_link("UK_THEFT_1968", "1")
    assert "legislation.gov.uk/ukpga/1968/60/section/1" in uk_info["official_section_url"]
    assert uk_info["jurisdiction"] == "UK"

    # EU resolution (EUR-Lex ELI deep link)
    eu_info = statute_linker.resolve_statute_link("EU_GDPR_2016", "5")
    assert "eur-lex.europa.eu/eli/reg/2016/679/art_5/oj" in eu_info["official_section_url"]
    assert eu_info["jurisdiction"] == "EU"

    # In-text citation linker
    text = "Defendant violated Section 1 of the Theft Act 1968 and processed data under GDPR Article 5."
    links = statute_linker.link_citations_in_text(text)
    assert len(links) >= 2
    act_ids = [l["act_id"] for l in links]
    assert "UK_THEFT_1968" in act_ids
    assert "EU_GDPR_2016" in act_ids

def test_expanded_us_statutes_retrieval():
    ledger = EvidenceLedger()
    retriever = LocalLegalRetriever(ledger)
    verifier = DeterministicVerifier(ledger)

    # 1. Section 230 CDA
    ev_230 = retriever.lookup_section("US_COMMUNICATIONS_1934", "230")
    assert ev_230 is not None
    assert "interactive computer service" in ev_230.text_span.lower()

    # 2. DMCA 512
    ev_dmca = retriever.lookup_section("US_DMCA_1998", "512")
    assert ev_dmca is not None
    assert "service provider" in ev_dmca.text_span.lower()

    # 3. FLSA Minimum Wage
    ev_flsa = retriever.lookup_section("US_FLSA_1938", "6")
    assert ev_flsa is not None
    assert "minimum hourly wage" in ev_flsa.text_span.lower()

    # Verify claim against ledger
    claim = Claim(
        claim_id="C_US_COMM_01",
        text="Section 230 of Communications Act protects interactive computer services from publisher liability.",
        claim_type="statutory",
        evidence_ids=[ev_230.evidence_id],
        citation_ids=[ev_230.locator]
    )
    verdict = verifier.verify_claim(claim)
    assert verdict.status == "PASS"

def test_expanded_uk_statutes_retrieval():
    ledger = EvidenceLedger()
    retriever = LocalLegalRetriever(ledger)
    verifier = DeterministicVerifier(ledger)

    # 1. POCA 2002 Money Laundering
    ev_poca = retriever.lookup_section("UK_POCA_2002", "327")
    assert ev_poca is not None
    assert "conceals criminal property" in ev_poca.text_span.lower()

    # 2. Online Safety Act 2023
    ev_osa = retriever.lookup_section("UK_ONLINE_SAFETY_2023", "7")
    assert ev_osa is not None
    assert "illegal content risk assessment" in ev_osa.text_span.lower()

    # 3. UCTA 1977
    ev_ucta = retriever.lookup_section("UK_UCTA_1977", "2")
    assert ev_ucta is not None
    assert "negligence" in ev_ucta.text_span.lower()

    claim = Claim(
        claim_id="C_UK_POCA_01",
        text="Section 327 of Proceeds of Crime Act 2002 criminalises concealing criminal property.",
        claim_type="statutory",
        evidence_ids=[ev_poca.evidence_id],
        citation_ids=[ev_poca.locator]
    )
    verdict = verifier.verify_claim(claim)
    assert verdict.status == "PASS"

def test_expanded_eu_statutes_retrieval():
    ledger = EvidenceLedger()
    retriever = LocalLegalRetriever(ledger)
    verifier = DeterministicVerifier(ledger)

    # 1. Data Act 2023
    ev_data = retriever.lookup_section("EU_DATA_ACT_2023", "3")
    assert ev_data is not None
    assert "connected products" in ev_data.text_span.lower()

    # 2. NIS 2 Directive
    ev_nis2 = retriever.lookup_section("EU_NIS2_DIR_2022", "21")
    assert ev_nis2 is not None
    assert "security of network and information systems" in ev_nis2.text_span.lower()

    # 3. Brussels I Recast
    ev_brussels = retriever.lookup_section("EU_BRUSSELS_I_RECAST_2012", "4")
    assert ev_brussels is not None
    assert "domiciled in a member state" in ev_brussels.text_span.lower()

    claim = Claim(
        claim_id="C_EU_DATA_01",
        text="Article 3 of Data Act establishes the obligation to make product data accessible to the user.",
        claim_type="statutory",
        evidence_ids=[ev_data.evidence_id],
        citation_ids=[ev_data.locator]
    )
    verdict = verifier.verify_claim(claim)
    assert verdict.status == "PASS"



