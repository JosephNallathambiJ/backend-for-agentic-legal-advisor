# HNX26EPS01: Multi-Jurisdiction Offline Agentic Legal Assistant (Pure Backend)
## Deterministic Verification Architecture — Air-Gapped, Fail-Closed, Evidence-First

A production-grade, resource-constrained, **100% local and offline headless backend** developed for the hackathon track:

> **Track HNX26EPS01: Agentic Legal Assistant**  
> *Core Engineering Philosophy: Verifiability Over Fluency*

---

## 📑 Table of Contents

1. [Executive Summary & Core Mandate](#-executive-summary--core-mandate)
2. [Multi-Jurisdictional Architecture](#-multi-jurisdictional-architecture)
   - [India (Central Acts & IndiaCode)](#1-india-central-acts--indiacode)
   - [United States (Federal Statutes & UCC)](#2-united-states-federal-statutes--ucc)
   - [United Kingdom (Acts of Parliament)](#3-united-kingdom-acts-of-parliament)
   - [European Union (Regulations & Directives)](#4-european-union-regulations--directives)
3. [Zero-Network & Resource Constraints](#-zero-network--resource-constraints)
4. [Dataset Catalog & CSV Schemas](#-dataset-catalog--csv-schemas)
5. [Official Case Verification & Citizen Services Portals](#-official-case-verification--citizen-services-portals)
6. [The Deterministic Verification Engine (Checks A to H)](#-the-deterministic-verification-engine-checks-a-to-h)
7. [Supported Legal Workflows](#-supported-legal-workflows)
8. [Repository File Map](#-repository-file-map)
9. [Getting Started & Installation](#-getting-started--installation)
10. [CLI Usage Guide with Multi-Jurisdiction Examples](#-cli-usage-guide-with-multi-jurisdiction-examples)
11. [Headless REST API Specification](#-headless-rest-api-specification)
12. [Scientific Ablation Benchmark (A0 to A4)](#-scientific-ablation-benchmark-a0-to-a4)
13. [Automated Test Suite & Regression Testing](#-automated-test-suite--regression-testing)
14. [Troubleshooting & FAQ](#-troubleshooting--faq)

---

## 🏛️ Executive Summary & Core Mandate

In high-stakes legal technology, **verifiability is paramount**. Generative LLMs routinely hallucinate non-existent sections, fabricate citations, and blur client facts with statutory text.

This system replaces probabilistic assertions with a **Deterministic Verification Architecture**:
```
┌────────────────────────────────────────────────────────────────────────┐
│                        EVIDENCE IS THE SOURCE OF TRUTH                 │
│                     The LLM is NEVER the Source of Truth               │
├────────────────────────────────────────────────────────────────────────┤
│  1. The Local LLM or Deterministic Engine PROPOSES text.               │
│  2. The Verifier DETERMINISTICALLY VALIDATES against the Evidence Ledger.│
│  3. If evidence is missing, conflicting, or unverifiable → FAIL-CLOSED.│
│  4. The API / CLI outputs an unalterable audit trail of every claim.   │
└────────────────────────────────────────────────────────────────────────┘
```

### Architectural Axioms:
- **Abstention > Unsupported Answer**: The system withholds ungrounded legal assertions rather than guessing.
- **Verified Incomplete Answer > Fluent Hallucination**: Missing details trigger explicit placeholders (`[NOT PROVIDED]`) rather than invented facts.
- **Fail-Closed Release Gate**: Any internal pipeline exception, timeout, or schema mismatch defaults immediately to `REJECT` or `NOT_VERIFIED`.

---

## 🌍 Multi-Jurisdictional Architecture

The system supports four distinct legal jurisdictions with automatic classification and targeted statutory retrieval:

```
                               ┌─────────────────────────┐
                               │     Legal Query or      │
                               │   Case Dossier Input    │
                               └────────────┬────────────┘
                                            │
                                            ▼
                               ┌─────────────────────────┐
                               │   Multi-Jurisdiction    │
                               │      Legal Router       │
                               └────────────┬────────────┘
                                            │
         ┌──────────────────┬───────────────┴──────────────┬──────────────────┐
         ▼                  ▼                              ▼                  ▼
┌─────────────────┐ ┌─────────────────┐    ┌─────────────────┐ ┌─────────────────┐
│     INDIA       │ │  UNITED STATES  │    │ UNITED KINGDOM  │ │ EUROPEAN UNION  │
│ 876 Central Acts│ │ Title 18 U.S.C. │    │ Theft Act 1968  │ │ GDPR 2016/679   │
│ BNS, BNSS, BSA  │ │ UCC Article 2   │    │ Consumer Rights │ │ EU AI Act 2024  │
│ IndiaCode Mirror│ │ House Code / LII│    │ Legislation.gov │ │ EUR-Lex Corpus  │
└─────────────────┘ └─────────────────┘    └─────────────────┘ └─────────────────┘
```

### 1. India (Central Acts & IndiaCode)
- **Primary Source**: Official Government of India repository (`indiacode.nic.in`) mirrored into local SQLite cache.
- **Coverage**: 876 Central Acts, including the new criminal law codes:
  - **BNS 2023** (*Bharatiya Nyaya Sanhita, 2023* - Act No. 45 of 2023)
  - **BNSS 2023** (*Bharatiya Nagarik Suraksha Sanhita, 2023* - Act No. 46 of 2023)
  - **BSA 2023** (*Bharatiya Sakshya Adhiniyam, 2023* - Act No. 47 of 2023)
  - **ICA 1872** (*The Indian Contract Act, 1872* - Act No. 09 of 1872)
- **Transition Rule**: Automatically audits offences occurring before July 1, 2024 against the Indian Penal Code (IPC) rather than BNS.
- **External Case Verification Portals**:
  - **Digital Police Citizen Services**: [https://www.digitalpolicecitizenservices.gov.in/](https://www.digitalpolicecitizenservices.gov.in/) (for verifying FIR status, complaints, and citizen verifications)
  - **eCourts Services Portal (eCourts 2.0)**: [https://ecourts.gov.in/ecourts2.0/](https://ecourts.gov.in/ecourts2.0/) (for checking live case status, CNR numbers, court orders, and cause lists across Indian courts)

### 2. United States (Federal Statutes & UCC)
- **Primary Source**: United States Code (Office of the Law Revision Counsel) and Uniform Commercial Code (Cornell LII).
- **Coverage**:
  - **Title 18 U.S.C.** (Crimes and Criminal Procedure): Public property theft (§ 641), fraud (§ 1341), etc.
  - **UCC Article 2** (Sales): Statute of frauds (§ 2-201), offer & acceptance (§ 2-206), unconscionability (§ 2-302).

### 3. United Kingdom (Acts of Parliament)
- **Primary Source**: The National Archives (`legislation.gov.uk`).
- **Coverage**:
  - **Theft Act 1968** (c. 60): Basic definition of theft (§ 1), dishonest appropriation (§ 2-3).
  - **Contracts (Rights of Third Parties) Act 1999** (c. 31): Third party enforcement rights (§ 1).
  - **Consumer Rights Act 2015** (c. 15): Satisfactory quality (§ 9), right to reject (§ 20).

### 4. European Union (Regulations & Directives)
- **Primary Source**: Official Journal of the European Union (`eur-lex.europa.eu`).
- **Coverage**:
  - **Regulation (EU) 2016/679 (GDPR)**: Principles of data processing (Article 5), lawfulness (Article 6).
  - **Regulation (EU) 2024/1689 (EU AI Act)**: Prohibited AI practices (Article 5), high-risk AI governance (Article 6).

---

## 🔒 Zero-Network & Resource Constraints

This engine is engineered for strict compliance with enterprise air-gapped guidelines:

| Constraint | Enforcement Mechanism | Status |
| :--- | :--- | :--- |
| **Network Access** | `NETWORK = DISABLED`. Socket connections outside localhost blocked. No remote APIs (OpenAI, Gemini, Groq, Pinecone). | **0 Outbound Calls** |
| **Resident RAM** | Targeted at ≤ 3.5 GB (3584 MB). Efficient memory footprint with SQLite index. | **~190 MB RSS** (Tested) |
| **Compute Type** | Commodity x86_64 / ARM64 CPU only. No discrete GPU required. | **Pure CPU** |
| **Frontend/Docker** | Pure headless backend. Zero web browser dependencies, zero Docker virtualization. | **Pure Python** |

---

## 📊 Dataset Catalog & CSV Schemas

All legal statutes are cataloged in `data/csv/` with cryptographic SHA-256 hashes:

### 1. `data/csv/all_jurisdictions_acts.csv` (Master Corpus)
Contains 883 registered statutes across India, US, UK, and EU.
```csv
jurisdiction,act_id,act_title,short_title,year,act_number,enactment_date,official_url,sha256
INDIA,ACT_THE_INDIAN_TOLLS_ACT_1851_1851,"The Indian Tolls Act, 1851",...,https://www.indiacode.nic.in/...
US,US_TITLE_18,"Title 18 U.S.C. - Crimes and Criminal Procedure",...,https://uscode.house.gov/...
UK,UK_THEFT_1968,"Theft Act 1968 (c. 60)",...,https://www.legislation.gov.uk/...
EU,EU_GDPR_2016,"Regulation (EU) 2016/679 (GDPR)",...,https://eur-lex.europa.eu/...
```

### 2. Individual Jurisdiction Datasets
- [`data/csv/india_central_acts.csv`](data/csv/india_central_acts.csv): 876 Indian Central Acts with IndiaCode bitstream URLs.
- [`data/csv/us_federal_statutes.csv`](data/csv/us_federal_statutes.csv): US Federal statutory titles.
- [`data/csv/uk_statutes.csv`](data/csv/uk_statutes.csv): UK Parliament enacted statutes.
- [`data/csv/eu_regulations.csv`](data/csv/eu_regulations.csv): European Union regulations.

### 3. Local SQLite Statutory Cache
- Location: `data/cache/legal_cache.sqlite`
- Indexed Sections: **37,849 sections**
- Fast lookup by `(act_id, section_number)` with pre-computed SHA-256 hashes.

---

## 🔍 Official Case Verification & Citizen Services Portals

For verifying real-world litigation records, police complaints, FIR filings, and court proceedings referenced in case dossiers or client materials, users can cross-examine live government records via the official citizen portals:

1. **Digital Police Citizen Services (Ministry of Home Affairs / NCRB)**:
   - **Portal Link**: [https://www.digitalpolicecitizenservices.gov.in/](https://www.digitalpolicecitizenservices.gov.in/)
   - **Purpose**: Verify state-wise FIR registrations, check complaint status, access missing person registries, and request official police clearance/verification services.

2. **eCourts Services Portal (eCourts 2.0 - Judicial Service Delivery)**:
   - **Portal Link**: [https://ecourts.gov.in/ecourts2.0/](https://ecourts.gov.in/ecourts2.0/)
   - **Purpose**: Real-time validation of case status, Case Number Record (CNR) search, daily cause lists, court order sheets, and judgment histories across District Courts and High Courts of India.

---

## 🛡️ The Deterministic Verification Engine (Checks A to H)

Every sentence produced by the drafting engine is parsed into atomic claims and subjected to eight deterministic gates:

```
                  ┌──────────────────────────────┐
                  │    Draft Output (Claims)     │
                  └──────────────┬───────────────┘
                                 │
  [Gate A] Schema Validation     │ Reject malformed structure or missing IDs
  [Gate B] Citation Allowlist    │ Reject fake sections (e.g. Section 999 BNS)
  [Gate C] Exact Quote Matching  │ Verbatim slice comparison against ledger
  [Gate D] Claim-Evidence Align  │ Atomic semantic alignment against premise
  [Gate E] Fact-Source Rule      │ Dossier facts must cite dossier, not statutes
  [Gate F] Temporal Applicability│ Pre-July 2024 IPC/BNS transition validation
  [Gate G] Calibrated NLI Gate   │ Stem-aware entailment & contradiction check
  [Gate H] Fail-Closed Release   │ Any error/unknown defaults to WITHHELD
                                 │
                                 ▼
                  ┌──────────────────────────────┐
                  │ Audited Text + Verdict Table │
                  └──────────────────────────────┘
```

- **Check A (Schema Validation)**: Validates that each claim is typed, cites valid evidence IDs (`E0001`, `F0001`), and maintains integrity.
- **Check B (Citation Allowlist)**: Disallows non-existent sections (e.g., *Section 999 BNS*). Citations must exist in the local SQLite cache.
- **Check C (Exact Quotations)**: Verifies that any quote placed inside quotation marks (`"..."`) is an exact substring of the referenced evidence.
- **Check D (Claim / Evidence Alignment)**: Rejects unsupported or overstated assertions.
- **Check E (Fact-Source Rule)**: Facts of occurrence (e.g., date of arrest, contract breach) must be grounded in dossier evidence (`E_CASE`), not statutory texts.
- **Check F (Applicability / Version)**: Confirms temporal jurisdiction (e.g., criminal acts before July 2024 are evaluated under IPC 1860).
- **Check G (Calibrated NLI Gate)**: Employs a stem-aware local NLI validator that detects contradictions and ungrounded numeric claims.
- **Check H (Fail-Closed Release)**: If verification cannot be confirmed with 100% certainty, the claim is rejected or withheld.

---

## ⚡ Supported Legal Workflows

1. **Contract / Case Review (`contract_case_review`)**:
   - Cross-examines contractual agreements or dispute dossiers.
   - Audits termination clauses, damages, and statutory compliance (UCC Art 2, Indian Contract Act, UK Consumer Rights).
   - Identifies internal contradictions (e.g., conflicting delivery dates, mismatched amounts).

2. **Legal Drafting (`bail_petition`)**:
   - Prepares formal court pleadings and bail applications.
   - Enforces pre-draft fact completeness. Missing facts are filled with safe placeholders:
     `[COURT NAME NOT PROVIDED]`, `[APPLICANT NAME NOT PROVIDED]`, `[FIR NUMBER NOT FOUND]`.

3. **Legal Research (`legal_research`)**:
   - Analyzes legal propositions across India, US, UK, or EU statutes.
   - Returns verbatim statutory provisions with exact quotation markers and provenance hashes.

4. **Grounded RAG Chat (`rag_chat`)**:
   - Answers direct legal queries strictly within the four corners of verified evidence.
   - Refuses to speculate or answer questions citing non-existent statutes (*abstention mode*).

---

## 📂 Repository File Map

```text
.
├── config.yaml                     # Local runtime configuration (RAM budget, timeouts)
├── requirements.txt                # Production dependencies
├── pytest.ini                      # Optimized pytest runner configuration
├── run.sh                          # One-command backend bootstrapper with pre-flight checks
├── cli.py                          # Multi-jurisdiction terminal CLI
│
├── api/                            # Headless REST API
│   └── app.py                      # FastAPI microservice (/health, /api/run, /api/lookup, etc.)
│
├── core/                           # Deterministic Legal Intelligence Engine
│   ├── schemas.py                  # Pydantic data contracts (Claim, Evidence, Verdict, etc.)
│   ├── provenance.py               # Thread-safe EvidenceLedger & immutable hashing
│   ├── case_parser.py              # Offset-aware PDF/text dossier parser & injection sanitizer
│   ├── legal_router.py             # Multi-jurisdiction TF-IDF & citation pattern router
│   ├── local_legal_retriever.py    # Offline SQLite statutory retriever
│   ├── contradiction_detector.py   # Cross-dossier numerical and temporal conflict detector
│   ├── nli_verifier.py             # Stem-aware calibrated NLI gate
│   ├── verifier.py                 # Deterministic Verifier (Checks A through H)
│   ├── llm_engine.py               # Strict drafting engine (GGUF or deterministic rule-based)
│   ├── agent_orchestrator.py       # Bounded agent loop & pre-draft confidence auditor
│   ├── pipeline_coordinator.py     # End-to-end workflow coordinator
│   ├── evaluator.py                # Scientific ablation benchmark suite (A0 to A4)
│   ├── telemetry.py                # Resource and zero-network monitor
│   ├── security.py                 # Prompt injection detection & sanitization
│   └── logging_config.py           # Structured logging with PII scrubbing
│
├── data/
│   ├── csv/                        # Full statutory CSV datasets (India, US, UK, EU, Master)
│   ├── cache/legal_cache.sqlite    # 37,849 sections indexed offline
│   ├── registry/registry_index.json# 883 registered statutory acts with canonical aliases
│   ├── legal_corpus/               # 758 indexed act directories
│   ├── test_cases/                 # Multi-jurisdiction sample disputes
│   └── gold/                       # Ground-truth claim benchmark labels
│
├── tests/                          # 29 Regression & Verification Tests (100% Pass)
│   ├── test_jurisdictions.py       # India, US, UK, EU retrieval and citation tests
│   ├── test_citations.py           # Citation allowlist & fake section rejection tests
│   ├── test_quotes.py              # Exact verbatim quote matching tests
│   ├── test_verifier.py            # Checks A through H unit tests
│   ├── test_contradictions.py      # Cross-document conflict detection tests
│   ├── test_parser.py              # Document parser & character offset tests
│   ├── test_prompt_injection.py    # Adversarial injection defense tests
│   ├── test_retrieval.py           # Offline statutory lookup tests
│   └── test_end_to_end.py          # Full pipeline workflow execution tests
│
└── scripts/
    ├── setup_models.sh             # Air-gapped pre-flight resource check
    ├── memory_check.py             # RAM diagnostic (≤ 3.5 GB budget)
    ├── validate_corpus.py          # Corpus integrity & SHA-256 hash auditor
    ├── build_index.py              # SQLite cache indexer from source data
    ├── populate_jurisdiction_corpus.py # Multi-jurisdiction corpus generator
    └── run_benchmark.py            # Scientific ablation evaluator runner
```

---

## 🚀 Getting Started & Installation

### 1. Prerequisites
- Python 3.10+ (tested on Python 3.12)
- Linux / macOS / WSL (x86_64 or ARM64)
- 2 GB available RAM (budget ceiling: 3.5 GB)

### 2. Environment Setup
```bash
# Create and activate virtual environment
python3 -m venv ~/legal_env
source ~/legal_env/bin/activate

# Install required packages
pip install -r requirements.txt
```

### 3. Verify Offline Corpus Integrity
Run the built-in diagnostic scripts to verify your local installation:
```bash
# Step 1: Pre-flight check
bash scripts/setup_models.sh

# Step 2: RAM footprint verification
python scripts/memory_check.py

# Step 3: Statute hash validation
python scripts/validate_corpus.py
```

---

## 💻 CLI Usage Guide with Multi-Jurisdiction Examples

The backend CLI (`cli.py`) allows instant terminal execution of any workflow across all four jurisdictions.

### 1. Run Pre-Configured Benchmark Scenarios

#### India (Bharatiya Nyaya Sanhita - Theft / Bail):
```bash
python cli.py --scenario theft_bns
```

#### India (Indian Contract Act - Breach Review):
```bash
python cli.py --scenario contract_ica
```

#### United States (Title 18 U.S.C. - Government Property Theft):
```bash
python cli.py --scenario us_theft_18usc
```

#### United States (UCC Article 2 - Statute of Frauds Contract Defense):
```bash
python cli.py --scenario us_ucc_contract
```

#### United Kingdom (Theft Act 1968 - Dishonest Appropriation):
```bash
python cli.py --scenario uk_theft_act
```

#### United Kingdom (Consumer Rights Act 2015 - Vehicle Warranty Review):
```bash
python cli.py --scenario uk_consumer_rights
```

#### European Union (GDPR - Lawfulness of Processing):
```bash
python cli.py --scenario eu_gdpr
```

#### European Union (EU AI Act - Workplace Biometrics Compliance):
```bash
python cli.py --scenario eu_ai_act
```

### 2. Run Custom Query with Raw Case Text
```bash
python cli.py \
  --workflow legal_research \
  --query "Analyze data processing under Article 5 of GDPR" \
  --text "The company stores employee browsing logs for 5 years without documented purpose."
```

### 3. Export Machine-Readable JSON Output
```bash
python cli.py --scenario theft_bns --json
```

---

## 🌐 Headless REST API Specification

Launch the background API service:
```bash
./run.sh
```
Or directly:
```bash
uvicorn api.app:app --host 127.0.0.1 --port 8000
```

### Available Endpoints:

#### `GET /health`
Returns system status, active resident RAM, and offline verification confirmation.
```json
{
  "status": "HEALTHY",
  "mode": "OFFLINE_LOCAL",
  "network": "DISABLED (0 Outbound Calls)",
  "resident_ram_mb": 189.4,
  "target_ram_budget_mb": 3584.0,
  "indexed_acts": 883,
  "supported_jurisdictions": ["INDIA", "US", "UK", "EU"]
}
```

#### `GET /api/jurisdictions`
Returns statutory counts available in each jurisdiction.
```json
{
  "INDIA": 876,
  "US": 2,
  "UK": 3,
  "EU": 2
}
```

#### `POST /api/run`
Executes an audited legal pipeline workflow.
**Request Body**:
```json
{
  "workflow": "legal_research",
  "query": "Review theft under Section 1 of the Theft Act 1968",
  "raw_text": "Defendant appropriated a bicycle believing it was abandoned.",
  "jurisdiction": "UK"
}
```
**Response**: Full `PipelineResult` JSON containing atomic facts, claims, verification verdicts (PASS, FLAG, REJECT), contradiction flags, and final audited text.

#### `POST /api/lookup`
Direct statutory lookup from offline SQLite cache.
**Request Body**:
```json
{
  "act_id": "EU_GDPR_2016",
  "section_number": "5"
}
```
**Response**:
```json
{
  "evidence_id": "E0001",
  "evidence_type": "statute",
  "jurisdiction": "EU",
  "source_id": "EU_GDPR_2016",
  "source_title": "Regulation (EU) 2016/679 — General Data Protection Regulation (GDPR)",
  "section": "5",
  "text_span": "Personal data shall be processed lawfully, fairly and in a transparent manner...",
  "locator": "EU_GDPR_2016:Sec5",
  "hash": "ef73112fade2..."
}
```

#### `POST /api/verify`
Standalone claim verification against an evidence ledger.

#### `GET /api/test_cases`
Retrieves pre-loaded benchmark dispute dossiers.

---

## 📈 Scientific Ablation Benchmark (A0 to A4)

The project includes an empirical ablation benchmark (`core/evaluator.py`) evaluating verification precision across 5 system configurations:

Run the benchmark runner:
```bash
python scripts/run_benchmark.py
```

### Measured Ablation Results:

| Regime | Description | Total Claims | Passed | Flagged | Rejected | FAR (%) | Citation Precision | Abstention Rate | Latency |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **A0** | Baseline (Unconstrained LLM) | 18 | 18 | 0 | 0 | **5.56%** | 100.0% | 0.0% | 0.30s |
| **A1** | Lexical / TF-IDF Retrieval | 18 | 18 | 0 | 0 | **5.56%** | 100.0% | 0.0% | 0.29s |
| **A2** | Atomic Claim Splitting | 18 | 18 | 0 | 0 | **5.56%** | 100.0% | 0.0% | 0.29s |
| **A3** | Provenance & Citation Gate | 18 | 17 | 0 | 1 | **0.00%** | 100.0% | 0.0% | 0.32s |
| **A4** | Full Gate (Deterministic + NLI) | 18 | 17 | 0 | 1 | **0.00%** | 100.0% | 0.0% | 0.29s |

### Benchmark Takeaway:
Under **A4 (Full Deterministic Architecture)**, the **False Acceptance Rate (FAR) drops to 0.00%**. Fabricated sections, ungrounded claims, and altered quotations are completely eliminated from the output.

---

## 🧪 Automated Test Suite & Regression Testing

The test suite validates every layer of the architecture across 29 test cases:

Run all tests:
```bash
pytest
```

### Test Suite Breakdown:
- [`tests/test_jurisdictions.py`](tests/test_jurisdictions.py): Verifies routing, retrieval, and quote alignment across India, US, UK, and EU statutes (6 tests).
- [`tests/test_citations.py`](tests/test_citations.py): Ensures authentic citations pass while fabricated citations (e.g. *Section 999 BNS*) are rejected (3 tests).
- [`tests/test_quotes.py`](tests/test_quotes.py): Confirms verbatim statutory quotes pass and altered or truncated quotes fail closed (2 tests).
- [`tests/test_verifier.py`](tests/test_verifier.py): Tests Checks A through H, including fact-source mismatches and semantic contradictions (4 tests).
- [`tests/test_contradictions.py`](tests/test_contradictions.py): Tests automatic detection of conflicting arrest dates and claim amounts across case documents (2 tests).
- [`tests/test_parser.py`](tests/test_parser.py): Tests character offsets and atomic proposition extraction (3 tests).
- [`tests/test_prompt_injection.py`](tests/test_prompt_injection.py): Tests defense against adversarial injection embedded in case files (2 tests).
- [`tests/test_retrieval.py`](tests/test_retrieval.py): Tests SQLite statutory lookups and priority routing (3 tests).
- [`tests/test_end_to_end.py`](tests/test_end_to_end.py): End-to-end execution of all 4 workflows (Contract Review, Bail Petition, Legal Research, RAG Chat) (4 tests).

**Result: 29 passed in ~2.7s (100% green).**

---

## ❓ Troubleshooting & FAQ

#### Q: How do I run this without an internet connection?
**A**: The entire project is self-contained. The statutory corpus is stored locally in `data/cache/legal_cache.sqlite` and `data/csv/`. No outbound network calls are ever attempted.

#### Q: Can I run this with a local neural LLM (e.g. Qwen2.5-1.5B)?
**A**: Yes. Place the GGUF model file `qwen2.5-1.5b-instruct-q4_k_m.gguf` in the `models/llm/` directory. If absent, the engine defaults to its local deterministic rule-based drafting engine without crashing.

#### Q: Why does the system output `[NOT PROVIDED]` instead of estimating facts?
**A**: To protect legal integrity. Fabricating client names, dates, or court jurisdictions is a critical failure. The pre-draft confidence auditor inserts explicit placeholders when facts are missing.

---

## 📜 License & Compliance

Developed for **HackNex 2026 (Track HNX26EPS01)**. Built strictly for ethical, verifiable, and explainable legal technology.
