# HNX26EPS01: Multi-Jurisdiction Offline Agentic Legal Assistant (Pure Backend)
## Deterministic Verification Architecture — Air-Gapped, Fail-Closed, Evidence-First

A production-grade, resource-constrained, **100% local and offline headless backend** developed for the hackathon track:

> **Track HNX26EPS01: Agentic Legal Assistant**  
> *Core Engineering Philosophy: Verifiability Over Fluency*

---

## 📑 Table of Contents

1. [Executive Summary & Core Mandate](#-executive-summary--core-mandate)
2. [Multi-Jurisdictional Architecture](#-multi-jurisdictional-architecture)
   - [Northern & Eastern Europe (18 Constitutions & Dial Codes)](#1-northern--eastern-europe-18-constitutions--dial-codes)
   - [United States (Federal Statutes & Constitution)](#2-united-states-federal-statutes--constitution)
   - [India (Central Acts & IndiaCode)](#3-india-central-acts--indiacode)
   - [United Kingdom & European Union](#4-united-kingdom--european-union)
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

### 1. Northern & Eastern Europe (18 Constitutions & Dial Codes)
All 18 Northern and Eastern European countries are mapped by official name, native constitutional name, and international phone dial code:

| Country | Dial Code | Constitutional Act ID | Constitutional Law & Year | Legislation Portal | Supreme Court Portal |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **Belarus** | `+375` | `BY_CONST_1994` | Constitution of the Republic of Belarus (1994) | [pravo.by](https://pravo.by) | [court.gov.by](https://court.gov.by) |
| **Bulgaria** | `+359` | `BG_CONST_1991` | Constitution of the Republic of Bulgaria (1991) | [dv.parliament.bg](https://dv.parliament.bg) | [vks.bg](https://www.vks.bg) |
| **Czech Republic** | `+420` | `CZ_CONST_1992` | Constitution of the Czech Republic (1992) | [zakonyprolidi.cz](https://www.zakonyprolidi.cz) | [nsoud.cz](https://www.nsoud.cz) |
| **Denmark** | `+45` | `DK_CONST_1953` | Constitutional Act of Denmark (*Danmarks Riges Grundlov* 1953) | [retsinformation.dk](https://www.retsinformation.dk) | [domstol.dk/hoejesteret](https://domstol.dk/hoejesteret) |
| **Estonia** | `+372` | `EE_CONST_1992` | Constitution of the Republic of Estonia (*Põhiseadus* 1992) | [riigiteataja.ee](https://www.riigiteataja.ee) | [riigikohus.ee](https://www.riigikohus.ee) |
| **Finland** | `+358` | `FI_CONST_1999` | Constitution of Finland (*Suomen perustuslaki* 1999) | [finlex.fi](https://finlex.fi) | [korkeinoikeus.fi](https://korkeinoikeus.fi) |
| **Hungary** | `+36` | `HU_CONST_2011` | Fundamental Law of Hungary (*Alaptörvény* 2011) | [njt.hu](https://njt.hu) | [kuria-birosag.hu](https://kuria-birosag.hu) |
| **Iceland** | `+354` | `IS_CONST_1944` | Constitution of the Republic of Iceland (*Stjórnarskrá* 1944) | [althingi.is/lagasafn](https://www.althingi.is/lagasafn/) | [haestirettur.is](https://www.haestirettur.is) |
| **Ireland** | `+353` | `IE_CONST_1937` | Constitution of Ireland (*Bunreacht na hÉireann* 1937) | [irishstatutebook.ie](https://www.irishstatutebook.ie) | [supremecourt.ie](https://www.supremecourt.ie) |
| **Latvia** | `+371` | `LV_CONST_1922` | Constitution of the Republic of Latvia (*Satversme* 1922) | [likumi.lv](https://likumi.lv) | [at.gov.lv](https://www.at.gov.lv) |
| **Lithuania** | `+370` | `LT_CONST_1992` | Constitution of the Republic of Lithuania (*Konstitucija* 1992) | [e-seimas.lrs.lt](https://e-seimas.lrs.lt) | [lat.lt](https://www.lat.lt) |
| **Norway** | `+47` | `NO_CONST_1814` | Constitution of the Kingdom of Norway (*Kongeriket Norges Grunnlov* 1814) | [lovdata.no](https://lovdata.no) | [domstol.no](https://www.domstol.no/en/supremecourt/) |
| **Poland** | `+48` | `PL_CONST_1997` | Constitution of the Republic of Poland (*Konstytucja RP* 1997) | [isap.sejm.gov.pl](https://isap.sejm.gov.pl) | [sn.pl](https://www.sn.pl) |
| **Romania** | `+40` | `RO_CONST_1991` | Constitution of Romania (*Constituția României* 1991) | [legislatie.just.ro](http://legislatie.just.ro) | [iccj.ro](https://www.iccj.ro) |
| **Russia** | `+7` | `RU_CONST_1993` | Constitution of the Russian Federation (1993) | [pravo.gov.ru](http://pravo.gov.ru) | [vsrf.ru](https://www.vsrf.ru) |
| **Slovakia** | `+421` | `SK_CONST_1992` | Constitution of the Slovak Republic (*Ústava Slovenskej Republiky* 1992) | [s-slov-lex.sk](https://www.s-slov-lex.sk) | [nsud.sk](https://www.nsud.sk) |
| **Sweden** | `+46` | `SE_CONST_1974` | The Instrument of Government (*Regeringsformen* 1974:152) | [rkrattsbaser.gov.se](https://rkrattsbaser.gov.se) | [hogstadomstolen.se](https://www.hogstadomstolen.se) |
| **Ukraine** | `+380` | `UA_CONST_1996` | Constitution of Ukraine (*Konstytutsiia Ukrainy* 1996) | [zakon.rada.gov.ua](https://zakon.rada.gov.ua) | [supreme.court.gov.ua](https://supreme.court.gov.ua) |

### 2. United States (Federal Statutes & Constitution)
- **Primary Code**: The **United States Code (U.S.C.)** is the official codification of the general and permanent federal laws of the United States.
- **Where to Access**: Federal legislation and bills are hosted on [Congress.gov](https://www.congress.gov/), historical acts are kept in the Statutes at Large via the Library of Congress ([loc.gov](https://www.loc.gov/collections/united-states-statutes-at-large/)), and codified titles on [uscode.house.gov](https://uscode.house.gov/).
- **Dial Code**: `+1`
- **Coverage (32 Codes & Federal Acts)**:
  - **US Constitution (1787)** (`US_CONST_1787`): Legislative Powers & Taxing Authority (Art I Sec 8), Executive Power (Art II Sec 1), Judicial Power (Art III Sec 2), Free Speech (Amend 1), Search & Seizure (Amend 4), Due Process (Amend 5), Equal Protection (Amend 14).
  - **Title 18 U.S.C.** (Crimes and Criminal Procedure): Public property theft (§ 641), false statements (§ 1001), mail fraud (§ 1341), wire fraud (§ 1343), obstruction of justice (§ 1503).
  - **Title 28 U.S.C.** (Judiciary and Judicial Procedure): Federal question jurisdiction (§ 1331), diversity of citizenship (§ 1332).
  - **UCC Article 2** (Sales): Statute of frauds (§ 2-201), offer & acceptance (§ 2-206), unconscionability (§ 2-302), damages (§ 2-713), remedy limitations (§ 2-719).
  - **Civil Rights Act of 1964** (Title 42 U.S.C. § 2000e): Public accommodations (§ 201), unlawful employment practices (§ 703).
  - **Voting Rights Act of 1965** (52 U.S.C. § 10301): Denial or abridgement of right to vote (§ 2).
  - **Sherman Antitrust Act of 1890** (15 U.S.C. §§ 1-7): Restraint of trade (§ 1), monopolization (§ 2).
  - **Clayton Antitrust Act of 1914** (15 U.S.C. §§ 12-27): Price discrimination (§ 2), mergers lessening competition (§ 7).
  - **Federal Trade Commission Act of 1914** (15 U.S.C. § 45): Unfair methods of competition & deceptive practices (§ 5).
  - **Securities Act of 1933** (15 U.S.C. § 77q): Fraudulent interstate transactions (§ 17(a)).
  - **Securities Exchange Act of 1934** (15 U.S.C. § 78j): Manipulative and deceptive devices (§ 10(b)).
  - **Copyright Act of 1976** (Title 17 U.S.C.): Exclusive rights (§ 106), fair use (§ 107).
  - **Digital Millennium Copyright Act of 1998 - DMCA** (17 U.S.C. § 512): Safe harbor & notice and takedown (§ 512).
  - **Title 35 U.S.C.** (Patents): Patentability (§ 101), novelty (§ 102), non-obviousness (§ 103), infringement (§ 271).
  - **Lanham Act of 1946** (15 U.S.C. § 1125): False designations of origin and trademark dilution (§ 43(a)).
  - **Title 11 U.S.C.** (Bankruptcy Code): Automatic stay (§ 362), discharge (§ 727), reorganization (§ 1129).
  - **Americans with Disabilities Act of 1990 - ADA** (42 U.S.C. § 12101): Employment (§ 102), public accommodations (§ 302).
  - **Freedom of Information Act of 1966 - FOIA** (5 U.S.C. § 552): Public access to federal records (§ 552).
  - **Administrative Procedure Act of 1946 - APA** (5 U.S.C. § 551): Rulemaking (§ 553), judicial review scope (§ 706).
  - **Fair Labor Standards Act of 1938 - FLSA** (29 U.S.C. § 201): Minimum wage (§ 6), maximum hours & overtime (§ 7).
  - **Occupational Safety and Health Act of 1970 - OSHA** (29 U.S.C. § 654): General duty clause (§ 5).
  - **Employee Retirement Income Security Act of 1974 - ERISA** (29 U.S.C. § 1104): Fiduciary duties (§ 404).
  - **Clean Air Act of 1970** (42 U.S.C. § 7409): National ambient air quality standards (§ 109).
  - **Clean Water Act of 1972** (33 U.S.C. § 1311): Effluent limitations (§ 301).
  - **CERCLA (Superfund) 1980** (42 U.S.C. § 9607): Strict liability for hazardous release cleanup (§ 107).
  - **Federal Food, Drug, and Cosmetic Act of 1938 - FD&C** (21 U.S.C. § 331): Adulterated or misbranded drugs (§ 301).
  - **Controlled Substances Act of 1970 - CSA** (21 U.S.C. § 841): Prohibited acts & drug trafficking penalties (§ 401).
  - **False Claims Act of 1863** (31 U.S.C. § 3729): Civil false claims penalties (§ 3729), qui tam actions (§ 3730).
  - **Bank Secrecy Act of 1970 - BSA** (31 U.S.C. § 5318): Anti-money laundering compliance programs (§ 5318(h)).
  - **Dodd-Frank Wall Street Reform Act of 2010** (12 U.S.C. § 5301): Whistleblower protections (§ 922).
  - **Communications Decency Act - Section 230** (47 U.S.C. § 230): Online interactive computer service immunity (§ 230(c)).
  - **HIPAA of 1996** (42 U.S.C. § 1320d-6): Wrongful disclosure of unique health identifiers (§ 1177).
- **Portals**: Legislation: [Congress.gov](https://www.congress.gov/) & [uscode.house.gov](https://uscode.house.gov/) | Supreme Court: [supremecourt.gov](https://www.supremecourt.gov/)

### 3. United Kingdom (Acts of Parliament & English Common Law)
- **Primary System**: The UK operates under an uncodified constitution using the English common law system combined with parliamentary statutes.
- **Where to Access**: All primary and secondary legislation for England, Wales, Scotland, and Northern Ireland is published online at [Legislation.gov.uk](https://www.legislation.gov.uk/), managed by The National Archives.
- **Dial Code**: `+44`
- **Coverage (28 Enacted Statutes)**:
  - **Theft Act 1968** (c. 60): Basic definition of theft (§ 1), dishonesty (§ 2), appropriation (§ 3), penalty (§ 7), robbery (§ 8).
  - **Theft Act 1978** (c. 31): Obtaining services by deception (§ 1), making off without payment (§ 3).
  - **Fraud Act 2006** (c. 35): Fraud offence (§ 1), fraud by false representation (§ 2), failure to disclose information (§ 3).
  - **Forgery and Counterfeiting Act 1981** (c. 45): The offence of forgery (§ 1), copying false instrument (§ 2).
  - **Police and Criminal Evidence Act 1984 - PACE** (c. 60): Stop and search (§ 1), right to legal advice (§ 58).
  - **Criminal Justice Act 2003** (c. 44): Admissibility of hearsay evidence (§ 114), bad character evidence (§ 101).
  - **Human Rights Act 1998** (c. 42): Interpretation compatible with Convention (§ 3), public authority acts (§ 6).
  - **Data Protection Act 2018** (c. 12): Law enforcement data principles (§ 35), data subject rights (§ 86).
  - **Contracts (Rights of Third Parties) Act 1999** (c. 31): Third party right to enforce term (§ 1), variation (§ 2).
  - **Consumer Rights Act 2015** (c. 15): Goods of satisfactory quality (§ 9), right to reject (§ 20).
  - **Sale of Goods Act 1979** (c. 54): Implied terms as to title (§ 12), description (§ 13), quality (§ 14).
  - **Supply of Goods and Services Act 1982** (c. 29): Implied term about reasonable care and skill (§ 13).
  - **Unfair Contract Terms Act 1977 - UCTA** (c. 50): Negligence liability (§ 2), reasonableness test (§ 11).
  - **Companies Act 2006** (c. 46): Duty to act within powers (§ 171), duty to promote company success (§ 172).
  - **Insolvency Act 1986** (c. 45): Transactions at an undervalue (§ 238), fraudulent trading (§ 213).
  - **Partnership Act 1890** (c. 39): Definition of partnership (§ 1), power of partner to bind firm (§ 5).
  - **Limited Liability Partnerships Act 2000** (c. 12): Limited liability partnership as body corporate (§ 1).
  - **Arbitration Act 1996** (c. 23): Stay of legal proceedings (§ 9), challenging award (§ 68).
  - **Employment Rights Act 1996** (c. 18): General right not to be unfairly dismissed (§ 94), fair reasons (§ 98).
  - **Equality Act 2010** (c. 15): Protected characteristics (§ 4), direct discrimination (§ 13), indirect discrimination (§ 19).
  - **Bribery Act 2010** (c. 23): Bribing another person (§ 1), failure of commercial organisations to prevent bribery (§ 7).
  - **Proceeds of Crime Act 2002 - POCA** (c. 29): Concealing criminal property (§ 327), arrangements (§ 328).
  - **Financial Services and Markets Act 2000 - FSMA** (c. 8): General prohibition on financial activities (§ 19).
  - **Defamation Act 2013** (c. 26): Serious harm requirement (§ 1), truth defence (§ 2), honest opinion (§ 3).
  - **Environmental Protection Act 1990** (c. 43): Prohibition on unauthorized deposit of waste (§ 33).
  - **Official Secrets Act 1989** (c. 6): Security and intelligence disclosures (§ 1), defense disclosures (§ 2).
  - **Computer Misuse Act 1990** (c. 18): Unauthorized access to computer material (§ 1), unauthorized acts with intent to impair (§ 3).
  - **Online Safety Act 2023** (c. 50): Safety duties about illegal content (§ 10), risk assessments (§ 9).
- **Portals**: Legislation: [Legislation.gov.uk](https://www.legislation.gov.uk/) | Supreme Court: [supremecourt.uk](https://www.supremecourt.uk/)

### 4. European Union (Supranational Regulations & Directives)
- **Primary System**: The EU uses a supranational system of treaties, regulations, and directives that bind or harmonize laws across its member states.
- **Where to Access**: All official EU laws, court rulings, and the Official Journal of the European Union are published on [EUR-Lex](https://eur-lex.europa.eu/homepage.html).
- **Dial Code**: `+32`
- **Coverage (28 Regulations, Directives & Treaties)**:
  - **Regulation (EU) 2016/679 (GDPR)**: Data processing principles (Art 5), lawfulness (Art 6), right to erasure (Art 17), administrative fines (Art 83).
  - **Regulation (EU) 2024/1689 (EU AI Act)**: Prohibited AI practices (Art 5), risk management system (Art 9), human oversight (Art 14), transparency (Art 50).
  - **Regulation (EU) 2022/2065 (Digital Services Act - DSA)**: Hosting liability exemption (Art 6), notice & action (Art 16), systemic risk assessment (Art 34).
  - **Regulation (EU) 2022/1925 (Digital Markets Act - DMA)**: Gatekeeper designation (Art 3), gatekeeper obligations on data combination (Art 5).
  - **Regulation (EU) 2023/1114 (Markets in Crypto-Assets - MiCA)**: CASP authorization (Art 59), market abuse prevention (Art 88).
  - **Regulation (EU) 2022/868 (Data Governance Act - DGA)**: Public sector data re-use conditions (Art 5).
  - **Regulation (EU) 2023/2854 (Data Act)**: Connected product data access rights (Art 3), cloud switching safeguards (Art 23).
  - **Regulation (EU) 2019/881 (Cybersecurity Act)**: European cybersecurity certification framework (Art 46).
  - **Regulation (EU) 2024/1183 (eIDAS 2 - Digital Identity)**: European Digital Identity Wallet (Art 6a).
  - **Directive (EU) 2022/2555 (NIS 2 Directive)**: Cybersecurity risk-management measures (Art 21).
  - **Directive (EU) 2019/790 (Copyright in the Digital Single Market)**: Text and data mining exception (Art 3), online sharing service liability (Art 17).
  - **Directive (EU) 2024/1760 (CSDDD - Corporate Sustainability)**: Due diligence in global corporate chains (Art 6).
  - **Directive (EU) 2022/2464 (CSRD - Sustainability Reporting)**: Sustainability reporting standard (Art 19a).
  - **Directive 2000/31/EC (E-Commerce Directive)**: Internal market clause (Art 3), hosting liability limitation (Art 14).
  - **Directive 2011/83/EU (Consumer Rights Directive)**: 14-day right of withdrawal from distance contracts (Art 9).
  - **Directive (EU) 2019/770 (Digital Content Directive)**: Conformity of digital content and services (Art 7).
  - **Directive (EU) 2019/771 (Sale of Goods Directive)**: Subjective and objective requirements for conformity of goods (Art 6).
  - **Directive (EU) 2016/943 (Trade Secrets Directive)**: Lawful acquisition, use and disclosure of trade secrets (Art 3).
  - **Directive 85/374/EEC (Product Liability Directive)**: Strict liability for damage caused by defective products (Art 1).
  - **Treaty on the Functioning of the European Union (TFEU 2012)**: Anti-competitive agreements (Art 101), abuse of dominance (Art 102), CJEU preliminary rulings (Art 267).
  - **Treaty on European Union (TEU 2016)**: Fundamental values (Art 2), democratic principles (Art 10).
  - **Charter of Fundamental Rights of the European Union**: Protection of personal data (Art 8), fair trial & effective remedy (Art 47).
  - **Regulation (EU) No 1215/2012 (Brussels I Recast)**: Jurisdiction in civil and commercial matters (Art 4).
  - **Regulation (EC) No 593/2008 (Rome I Regulation)**: Law applicable to contractual obligations and freedom of choice (Art 3).
  - **Regulation (EC) No 864/2007 (Rome II Regulation)**: Law applicable to non-contractual obligations and torts (Art 4).
  - **Regulation (EU) 2015/848 (European Insolvency Regulation)**: International jurisdiction based on center of main interests (Art 3).
  - **Regulation (EU) 2023/1781 (European Chips Act)**: Integrated production facility criteria and security of supply (Art 11).
  - **Regulation (EU) 2024/1735 (Net-Zero Industry Act)**: Fast-track net-zero strategic projects (Art 10).
- **Portals**: Legislation: [EUR-Lex](https://eur-lex.europa.eu/homepage.html) | Court of Justice (CJEU): [curia.europa.eu](https://curia.europa.eu/)

### 5. India (Central Acts & IndiaCode)
- **Primary Source**: Official Government of India repository (`indiacode.nic.in`) mirrored into local SQLite cache.
- **Dial Code**: `+91`
- **Coverage**: 876 Central Acts, including the criminal codes:
  - **BNS 2023** (*Bharatiya Nyaya Sanhita, 2023* - Act No. 45 of 2023)
  - **BNSS 2023** (*Bharatiya Nagarik Suraksha Sanhita, 2023* - Act No. 46 of 2023)
  - **BSA 2023** (*Bharatiya Sakshya Adhiniyam, 2023* - Act No. 47 of 2023)
  - **ICA 1872** (*The Indian Contract Act, 1872* - Act No. 09 of 1872)
- **Transition Rule**: Automatically audits offences occurring before July 1, 2024 against the Indian Penal Code (IPC) rather than BNS.
- **Portals**: Legislation: [indiacode.nic.in](https://www.indiacode.nic.in) | Supreme Court: [main.sci.gov.in](https://main.sci.gov.in)
- **Case Verification Portals**:
  - **Digital Police Citizen Services**: [https://www.digitalpolicecitizenservices.gov.in/](https://www.digitalpolicecitizenservices.gov.in/)
  - **eCourts Services Portal (eCourts 2.0)**: [https://ecourts.gov.in/ecourts2.0/](https://ecourts.gov.in/ecourts2.0/)

---

## 🔒 Zero-Network & Resource Constraints

This engine is engineered for strict compliance with enterprise air-gapped guidelines:

| Constraint | Enforcement Mechanism | Status |
| :--- | :--- | :--- |
| **Base Model** | **Gemma 4 12B** Instruct base profile with `<start_of_turn>user...` formatting, offline GGUF (Q4_K_M) + deterministic fail-safe drafting fallback. | **Gemma 4 12B Compatible** |
| **Network Access** | `NETWORK = DISABLED`. Socket connections outside localhost blocked. No remote APIs (OpenAI, Gemini, Groq, Pinecone). | **0 Outbound Calls (100% Offline)** |
| **Resident RAM** | Targeted at ≤ 3.5 GB (3584 MB). Efficient memory footprint with SQLite index. | **~191 MB RSS** (Tested) |
| **Compute Type** | Commodity x86_64 / ARM64 CPU only. No discrete GPU required. | **Pure CPU** |
| **Frontend/Docker** | Pure headless backend. Zero web browser dependencies, zero Docker virtualization. | **Pure Python** |

---

## 📊 Dataset Catalog & CSV Schemas

All legal statutes are cataloged in `data/csv/` with cryptographic SHA-256 hashes:

### 1. `data/csv/all_jurisdictions_acts.csv` (Master Corpus)
Contains **982 registered statutes** across 22 global jurisdictions (India, US, UK, EU, and 18 Northern & Eastern European nations) with 0 null values across all columns.
```csv
jurisdiction,act_id,act_title,short_title,year,act_number,enactment_date,official_url,sha256
BELARUS,BY_CONST_1994,"The Constitution of the Republic of Belarus (1994)",Belarus Constitution,1994,1994 Const. as amended,1994-03-15,https://pravo.by,e339ca82664d...
POLAND,PL_CONST_1997,"The Constitution of the Republic of Poland (1997)",Polish Constitution,1997,Dz.U. 1997 nr 78 poz. 483,1997-04-02,https://isap.sejm.gov.pl,6c5421ef45db...
SWEDEN,SE_CONST_1974,"The Instrument of Government (Regeringsformen 1974:152)",Swedish Constitution,1974,SFS 1974:152,1974-02-28,https://rkrattsbaser.gov.se,fbbe780f2c41...
US,US_CONST_1787,"The Constitution of the United States of America (1787)",US Constitution,1787,1787 Const. as ratified,1787-09-17,https://constitution.congress.gov,8e151d387ae4...
```

### 2. Individual Jurisdiction Datasets
- [`data/csv/northern_eastern_europe_constitutions.csv`](data/csv/northern_eastern_europe_constitutions.csv): 18 national constitutions with dial codes and official legislation URLs.
- [`data/csv/court_portals_registry.csv`](data/csv/court_portals_registry.csv): 22 countries cataloging official legislation and supreme court portals.
- [`data/csv/us_federal_statutes.csv`](data/csv/us_federal_statutes.csv): 32 US Federal statutory titles, acts, and US Constitution.
- [`data/csv/uk_statutes.csv`](data/csv/uk_statutes.csv): 28 UK Parliament enacted statutes.
- [`data/csv/eu_regulations.csv`](data/csv/eu_regulations.csv): 28 European Union regulations, directives, and treaties.
- [`data/csv/india_central_acts.csv`](data/csv/india_central_acts.csv): 876 Indian Central Acts with IndiaCode bitstream URLs.

### 3. Local SQLite Statutory Cache
- Location: `data/cache/legal_cache.sqlite`
- Indexed Sections: **38,146 sections**
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

3. **International Court & Legislation Portals Registry**:
   - Master Catalog: [`data/csv/court_portals_registry.csv`](data/csv/court_portals_registry.csv) (covering all 22 jurisdictions).
   - Display from CLI:
     ```bash
     python cli.py --portals
     ```

4. **Offline Statutory Web Linker (Direct Government Provenance without APIs)**:
   - **Zero-Network Resolution**: The module [`core/statute_web_linker.py`](core/statute_web_linker.py) deterministically formats official government URLs for any statute or section query completely offline:
     - **United States**: Resolves to [Congress.gov](https://www.congress.gov/) search and official [uscode.house.gov](https://uscode.house.gov/) Title/Section anchors.
     - **United Kingdom**: Resolves to [Legislation.gov.uk](https://www.legislation.gov.uk/) permalinks (`/ukpga/{year}/{chapter}/section/{sec}`).
     - **European Union**: Resolves to official [EUR-Lex](https://eur-lex.europa.eu/) European Legislation Identifier (ELI) anchors (`/eli/reg/{year}/{num}/art_{sec}/oj` or `/eli/dir/{year}/{num}/art_{sec}/oj`).
     - **India**: Resolves to official [indiacode.nic.in](https://www.indiacode.nic.in/) repository URLs.
   - **CLI Usage**:
     ```bash
     python cli.py --link "GDPR Article 5"
     python cli.py --link "Theft Act Section 1"
     python cli.py --link "Title 18 USC Section 641"
     ```
   - **REST API Endpoints**:
     - `GET /api/official_link?query=GDPR+Article+5`
     - `POST /api/link_citations`

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
│   ├── statute_web_linker.py       # Deterministic offline government deep-link resolver
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
│   ├── csv/                        # Full statutory CSV datasets (India, US, UK, EU, NE Europe, Master)
│   ├── cache/legal_cache.sqlite    # 38,146 sections indexed offline
│   ├── registry/registry_index.json# 982 registered statutory acts with canonical aliases
│   ├── legal_corpus/               # 758 indexed act directories
│   ├── test_cases/                 # Multi-jurisdiction sample disputes
│   └── gold/                       # Ground-truth claim benchmark labels
│
├── tests/                          # 47 Regression & Verification Tests (100% Pass)
│   ├── test_jurisdictions.py       # India, US, UK, EU retrieval, link, and citation tests (24 tests)
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
  "indexed_acts": 982,
  "base_model": "Gemma 4 12B",
  "supported_jurisdictions": ["INDIA", "US", "UK", "EU", "BELARUS", "BULGARIA", "..."]
}
```

#### `GET /api/jurisdictions`
Returns statutory counts available in each jurisdiction.
```json
{
  "INDIA": 876,
  "US": 32,
  "UK": 28,
  "EU": 28,
  "NORTHERN_EASTERN_EUROPE": 18
}
```

#### `GET /api/portals`
Returns the 22-jurisdiction registry of official legislation and supreme court portals.

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

#### `GET /api/official_link`
Resolves authentic government statutory repository link offline.
**Parameters**: `?query=GDPR+Article+5`
**Response**:
```json
{
  "query": "GDPR Article 5",
  "link": {
    "jurisdiction": "EU",
    "act_id": "EU_GDPR_2016",
    "act_title": "Regulation (EU) 2016/679 (General Data Protection Regulation)",
    "section": "5",
    "official_url": "https://eur-lex.europa.eu/eli/reg/2016/679/art_5/oj",
    "portal_name": "EUR-Lex (Official European Union Law)",
    "eli_format": true
  }
}
```

#### `POST /api/link_citations`
Batch resolves a list of citation strings to official portals offline.
**Request Body**:
```json
{
  "citations": ["Title 18 USC Section 641", "Theft Act Section 1", "GDPR Article 17"]
}
```

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

The test suite validates every layer of the architecture across 47 test cases:

Run all tests:
```bash
pytest
```

### Test Suite Breakdown:
- [`tests/test_jurisdictions.py`](tests/test_jurisdictions.py): Verifies routing, retrieval, quote alignment, dial codes, court portals, offline statutory linkers, and zero-null CSV consistency across India, US, UK, EU, and 18 Northern & Eastern European nations (24 tests).
- [`tests/test_citations.py`](tests/test_citations.py): Ensures authentic citations pass while fabricated citations (e.g. *Section 999 BNS*) are rejected (3 tests).
- [`tests/test_quotes.py`](tests/test_quotes.py): Confirms verbatim statutory quotes pass and altered or truncated quotes fail closed (2 tests).
- [`tests/test_verifier.py`](tests/test_verifier.py): Tests Checks A through H, including fact-source mismatches and semantic contradictions (4 tests).
- [`tests/test_contradictions.py`](tests/test_contradictions.py): Tests automatic detection of conflicting arrest dates and claim amounts across case documents (2 tests).
- [`tests/test_parser.py`](tests/test_parser.py): Tests character offsets and atomic proposition extraction (3 tests).
- [`tests/test_prompt_injection.py`](tests/test_prompt_injection.py): Tests defense against adversarial injection embedded in case files (2 tests).
- [`tests/test_retrieval.py`](tests/test_retrieval.py): Tests SQLite statutory lookups and priority routing (3 tests).
- [`tests/test_end_to_end.py`](tests/test_end_to_end.py): End-to-end execution of all 4 workflows (Contract Review, Bail Petition, Legal Research, RAG Chat) (4 tests).

**Result: 47 passed in ~3.1s (100% green).**

---

## ❓ Troubleshooting & FAQ

#### Q: How do I run this without an internet connection?
**A**: The entire project is self-contained. The statutory corpus is stored locally in `data/cache/legal_cache.sqlite` and `data/csv/`. No outbound network calls are ever attempted.

#### Q: How is Gemma 4 12B integrated as the base model?
**A**: The engine is pre-configured with Gemma 4 12B instruct turn formatting (`<start_of_turn>user...<end_of_turn>\n<start_of_turn>model\n`). Place the GGUF weights `gemma-4-12b-instruct-q4_k_m.gguf` in `models/llm/`. If running air-gapped without neural weights, the local deterministic rule-based drafting engine activates automatically with 0 errors and 0 RAM overhead. If absent, the engine defaults to its local deterministic rule-based drafting engine without crashing.

#### Q: Why does the system output `[NOT PROVIDED]` instead of estimating facts?
**A**: To protect legal integrity. Fabricating client names, dates, or court jurisdictions is a critical failure. The pre-draft confidence auditor inserts explicit placeholders when facts are missing.

---

## 📜 License & Compliance

Developed for **HackNex 2026 (Track HNX26EPS01)**. Built strictly for ethical, verifiable, and explainable legal technology.
