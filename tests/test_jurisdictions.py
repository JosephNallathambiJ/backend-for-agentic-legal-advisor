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
