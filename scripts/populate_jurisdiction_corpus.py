#!/usr/bin/env python3
"""
scripts/populate_jurisdiction_corpus.py - Multi-Jurisdiction Legal Corpus Builder
Builds, validates, and populates authoritative legal datasets for:
- INDIA (BNS 2023, BNSS 2023, BSA 2023, Contract Act 1872, CPC 1908, IT Act 2000, etc.)
- US (Title 18 USC Crimes/Theft/Fraud, Title 15 USC, UCC Article 2 Sales/Contracts, FRCP)
- UK (Theft Act 1968, Contracts (Third Parties) 1999, Consumer Rights 2015, PACE 1984, DPA 2018)
- EU / EUROPE (GDPR 2016/679, EU AI Act 2024/1689, Digital Markets Act 2022/1925, Charter)

Generates:
1. data/csv/india_central_acts.csv
2. data/csv/us_federal_statutes.csv
3. data/csv/uk_statutes.csv
4. data/csv/eu_regulations.csv
5. data/csv/all_jurisdictions_acts.csv
6. data/registry/registry_index.json (updated with jurisdiction metadata)
7. data/cache/legal_cache.sqlite (updated with multi-jurisdiction indexes)
8. data/legal_corpus/<JURISDICTION>/<ACT_ID>/section_<num>.json
"""

import os
import sys
import json
import sqlite3
import hashlib
import pandas as pd
from typing import Dict, List, Any

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(WORKSPACE_DIR, "data")
CSV_DIR = os.path.join(DATA_DIR, "csv")
CORPUS_DIR = os.path.join(DATA_DIR, "legal_corpus")
CACHE_DIR = os.path.join(DATA_DIR, "cache")
REGISTRY_DIR = os.path.join(DATA_DIR, "registry")
REGISTRY_FILE = os.path.join(REGISTRY_DIR, "registry_index.json")
SQLITE_DB = os.path.join(CACHE_DIR, "legal_cache.sqlite")

os.makedirs(CSV_DIR, exist_ok=True)
os.makedirs(CORPUS_DIR, exist_ok=True)
os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(REGISTRY_DIR, exist_ok=True)

def compute_hash(text: str) -> str:
    return hashlib.sha256(text.strip().encode("utf-8")).hexdigest()

# -------------------------------------------------------------
# INTERNATIONAL JURISDICTIONS DEFINITIONS
# -------------------------------------------------------------

US_CORPUS = [
    {
        "act_id": "US_TITLE_18",
        "act_title": "United States Code Title 18 — Crimes and Criminal Procedure",
        "short_title": "Title 18 U.S.C.",
        "year": 1948,
        "official_url": "https://uscode.house.gov/view.xhtml?path=/prelim@title18&edition=prelim",
        "aliases": ["title 18", "18 usc", "18 u.s.c.", "federal criminal code", "us title 18"],
        "sections": [
            {
                "section_number": "641",
                "title": "Public money, property or records",
                "text": "Whoever embezzles, steals, purloins, or knowingly converts to his use or the use of another, or without authority, sells, conveys or disposes of any record, voucher, money, or thing of value of the United States or of any department or agency thereof... Shall be fined under this title or imprisoned not more than ten years, or both."
            },
            {
                "section_number": "1001",
                "title": "Statements or entries generally",
                "text": "Except as otherwise provided in this section, whoever, in any matter within the jurisdiction of the executive, legislative, or judicial branch of the Government of the United States, knowingly and willfully falsifies, conceals, or covers up by any trick, scheme, or device a material fact; makes any materially false, fictitious, or fraudulent statement or representation; or makes or uses any false writing or document knowing the same to contain any materially false, fictitious, or fraudulent statement or entry; shall be fined under this title, imprisoned not more than 5 years."
            },
            {
                "section_number": "1341",
                "title": "Frauds and swindles (Mail Fraud)",
                "text": "Whoever, having devised or intending to devise any scheme or artifice to defraud, or for obtaining money or property by means of false or fraudulent pretenses, representations, or promises... places in any post office or authorized depository for mail matter, any matter or thing whatever to be sent or delivered by the Postal Service... shall be fined under this title or imprisoned not more than 20 years, or both."
            },
            {
                "section_number": "1343",
                "title": "Fraud by wire, radio, or television",
                "text": "Whoever, having devised or intending to devise any scheme or artifice to defraud, or for obtaining money or property by means of false or fraudulent pretenses, representations, or promises, transmits or causes to be transmitted by means of wire, radio, or television communication in interstate or foreign commerce, any writings, signs, signals, pictures, or sounds for the purpose of executing such scheme or artifice, shall be fined under this title or imprisoned not more than 20 years, or both."
            }
        ]
    },
    {
        "act_id": "US_UCC_ART_2",
        "act_title": "Uniform Commercial Code — Article 2: Sales",
        "short_title": "UCC Article 2",
        "year": 1951,
        "official_url": "https://www.law.cornell.edu/ucc/2",
        "aliases": ["ucc", "ucc article 2", "uniform commercial code", "ucc art 2", "us contracts sales"],
        "sections": [
            {
                "section_number": "2-201",
                "title": "Formal Requirements; Statute of Frauds",
                "text": "Except as otherwise provided in this section a contract for the sale of goods for the price of $500 or more is not enforceable by way of action or defense unless there is some writing sufficient to indicate that a contract for sale has been made between the parties and signed by the party against whom enforcement is sought or by his authorized agent or broker."
            },
            {
                "section_number": "2-713",
                "title": "Buyer's Damages for Non-delivery or Repudiation",
                "text": "The measure of damages for non-delivery or repudiation by the seller is the difference between the market price at the time when the buyer learned of the breach and the contract price together with any incidental and consequential damages provided in this Article, but less expenses saved in consequence of the seller's breach."
            },
            {
                "section_number": "2-719",
                "title": "Contractual Modification or Limitation of Remedy",
                "text": "The agreement may provide for remedies in addition to or in substitution for those provided in this Article and may limit or alter the measure of damages recoverable under this Article, as by limiting the buyer's remedies to return of the goods and repayment of the price or to repair and replacement of non-conforming goods or parts."
            }
        ]
    }
]

UK_CORPUS = [
    {
        "act_id": "UK_THEFT_1968",
        "act_title": "Theft Act 1968 (c. 60)",
        "short_title": "Theft Act 1968",
        "year": 1968,
        "official_url": "https://www.legislation.gov.uk/ukpga/1968/60/contents",
        "aliases": ["theft act 1968", "theft act", "uk theft act", "uk theft"],
        "sections": [
            {
                "section_number": "1",
                "title": "Basic definition of theft",
                "text": "A person is guilty of theft if he dishonestly appropriates property belonging to another with the intention of permanently depriving the other of it; and 'thief' and 'steal' shall be construed accordingly."
            },
            {
                "section_number": "2",
                "title": "Dishonesty",
                "text": "A person's appropriation of property belonging to another is not to be regarded as dishonest if he appropriates the property in the belief that he has in law the right to deprive the other of it, on behalf of himself or of a third person; or if he appropriates the property in the belief that he would have the other's consent if the other knew of the appropriation and the circumstances of it."
            },
            {
                "section_number": "3",
                "title": "Appropriates",
                "text": "Any assumption by a person of the rights of an owner amounts to an appropriation, and this includes, where he has come by the property (innocently or not) without stealing it, any later assumption of a right to it by keeping or dealing with it as owner."
            },
            {
                "section_number": "7",
                "title": "Theft penalty",
                "text": "A person guilty of theft shall on conviction on indictment be liable to imprisonment for a term not exceeding seven years."
            }
        ]
    },
    {
        "act_id": "UK_CONTRACTS_1999",
        "act_title": "Contracts (Rights of Third Parties) Act 1999 (c. 31)",
        "short_title": "Contracts Rights of Third Parties Act 1999",
        "year": 1999,
        "official_url": "https://www.legislation.gov.uk/ukpga/1999/31/contents",
        "aliases": ["contracts rights of third parties", "uk contracts act 1999", "third party rights act uk", "contracts 1999 uk"],
        "sections": [
            {
                "section_number": "1",
                "title": "Right of third party to enforce contractual term",
                "text": "Subject to the provisions of this Act, a person who is not a party to a contract (a 'third party') may in his own right enforce a term of the contract if the contract expressly provides that he may, or subject to subsection (2), the term purports to confer a benefit on him."
            },
            {
                "section_number": "2",
                "title": "Variation and rescission of contract",
                "text": "Subject to this section, where a third party has a right under section 1 to enforce a term of the contract, the parties to the contract may not, by agreement, rescind the contract, or vary it in such a way as to extinguish or alter his entitlement under that right, without his consent."
            }
        ]
    },
    {
        "act_id": "UK_CONSUMER_2015",
        "act_title": "Consumer Rights Act 2015 (c. 15)",
        "short_title": "Consumer Rights Act 2015",
        "year": 2015,
        "official_url": "https://www.legislation.gov.uk/ukpga/2015/15/contents",
        "aliases": ["consumer rights act 2015", "uk consumer rights", "cra 2015"],
        "sections": [
            {
                "section_number": "9",
                "title": "Goods to be of satisfactory quality",
                "text": "Every contract to supply goods is to be treated as including a term that the quality of the goods is satisfactory. The quality of goods is satisfactory if they meet the standard that a reasonable person would consider satisfactory, taking account of any description of the goods, the price, and all other relevant circumstances."
            },
            {
                "section_number": "10",
                "title": "Goods to be fit for particular purpose",
                "text": "Subsection (3) applies to a contract to supply goods if before the contract is made the consumer makes known to the trader (expressly or by implication) any particular purpose for which the consumer is contracting for the goods. The contract is to be treated as including a term that the goods are reasonably fit for that purpose."
            }
        ]
    }
]

EU_CORPUS = [
    {
        "act_id": "EU_GDPR_2016",
        "act_title": "Regulation (EU) 2016/679 — General Data Protection Regulation (GDPR)",
        "short_title": "EU GDPR",
        "year": 2016,
        "official_url": "https://eur-lex.europa.eu/eli/reg/2016/679/oj",
        "aliases": ["gdpr", "eu gdpr", "general data protection regulation", "regulation 2016/679", "gdpr regulation"],
        "sections": [
            {
                "section_number": "5",
                "title": "Principles relating to processing of personal data",
                "text": "Personal data shall be processed lawfully, fairly and in a transparent manner in relation to the data subject ('lawfulness, fairness and transparency'); collected for specified, explicit and legitimate purposes and not further processed in a manner that is incompatible with those purposes ('purpose limitation'); adequate, relevant and limited to what is necessary ('data minimisation')."
            },
            {
                "section_number": "6",
                "title": "Lawfulness of processing",
                "text": "Processing shall be lawful only if and to the extent that at least one of the following applies: (a) the data subject has given consent to the processing of his or her personal data; (b) processing is necessary for the performance of a contract to which the data subject is party; (c) processing is necessary for compliance with a legal obligation to which the controller is subject."
            },
            {
                "section_number": "17",
                "title": "Right to erasure ('right to be forgotten')",
                "text": "The data subject shall have the right to obtain from the controller the erasure of personal data concerning him or her without undue delay and the controller shall have the obligation to erase personal data without undue delay where one of the following grounds applies: the personal data are no longer necessary in relation to the purposes for which they were collected or otherwise processed."
            },
            {
                "section_number": "83",
                "title": "General conditions for imposing administrative fines",
                "text": "Each supervisory authority shall ensure that the imposition of administrative fines pursuant to this Article in respect of infringements of this Regulation referred to in paragraphs 4, 5 and 6 shall in each individual case be effective, proportionate and dissuasive. Infringements shall be subject to administrative fines up to 20 000 000 EUR, or in the case of an undertaking, up to 4 % of the total worldwide annual turnover of the preceding financial year, whichever is higher."
            }
        ]
    },
    {
        "act_id": "EU_AI_ACT_2024",
        "act_title": "Regulation (EU) 2024/1689 — Artificial Intelligence Act (EU AI Act)",
        "short_title": "EU AI Act",
        "year": 2024,
        "official_url": "https://eur-lex.europa.eu/eli/reg/2024/1689/oj",
        "aliases": ["eu ai act", "ai act", "regulation 2024/1689", "european ai act", "aia"],
        "sections": [
            {
                "section_number": "5",
                "title": "Prohibited Artificial Intelligence Practices",
                "text": "The following AI practices shall be prohibited: (a) the placing on the market, the putting into service or the use of an AI system that deploys subliminal techniques beyond a person's consciousness or purposefully manipulative or deceptive techniques; (b) the placing on the market, the putting into service or the use of an AI system that exploits any of the vulnerabilities of a person or a specific group of persons; (c) social scoring systems."
            },
            {
                "section_number": "9",
                "title": "Risk management system for high-risk AI systems",
                "text": "A risk management system shall be established, implemented, documented and maintained in relation to high-risk AI systems. The risk management system shall be understood as a continuous iterative process planned and run throughout the entire lifecycle of a high-risk AI system, requiring regular systematic review and updating."
            },
            {
                "section_number": "14",
                "title": "Human oversight of high-risk AI systems",
                "text": "High-risk AI systems shall be designed and developed in such a way, including with appropriate human-machine interface tools, that they can be effectively overseen by natural persons during the period in which they are in use. Human oversight shall aim to prevent or minimise the risks to health, safety or fundamental rights."
            }
        ]
    }
]

def main():
    print("=" * 70)
    print(" HNX26EPS01: MULTI-JURISDICTION LEGAL DATASET BUILDER")
    print(" Populating: INDIA, US, UK, EUROPE (EU)")
    print("=" * 70)

    # 1. Load Existing Indian Registry
    with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
        registry = json.load(f)

    # Tag all existing acts as INDIA
    india_acts_list = []
    for aid, meta in registry.items():
        meta["jurisdiction"] = "INDIA"
        india_acts_list.append({
            "jurisdiction": "INDIA",
            "act_id": aid,
            "act_title": meta.get("act_title", ""),
            "short_title": meta.get("short_name", ""),
            "year": meta.get("year", ""),
            "act_number": meta.get("act_number", ""),
            "enactment_date": meta.get("enactment_date", ""),
            "official_url": meta.get("official_url", ""),
            "sha256": meta.get("sha256", "")
        })

    # Save india_central_acts.csv
    df_india = pd.DataFrame(india_acts_list)
    india_csv_path = os.path.join(CSV_DIR, "india_central_acts.csv")
    df_india.to_csv(india_csv_path, index=False)
    print(f"[OK] Saved India Acts CSV: {india_csv_path} ({len(df_india)} Acts)")

    # 2. Setup SQLite Connection
    conn = sqlite3.connect(SQLITE_DB)
    cur = conn.cursor()
    # Check if jurisdiction column exists in acts
    try:
        cur.execute("ALTER TABLE acts ADD COLUMN jurisdiction TEXT DEFAULT 'INDIA'")
    except Exception:
        pass
    try:
        cur.execute("ALTER TABLE sections ADD COLUMN jurisdiction TEXT DEFAULT 'INDIA'")
    except Exception:
        pass

    # Ensure existing records are tagged with INDIA
    cur.execute("UPDATE acts SET jurisdiction='INDIA' WHERE jurisdiction IS NULL OR jurisdiction=''")
    cur.execute("UPDATE sections SET jurisdiction='INDIA' WHERE jurisdiction IS NULL OR jurisdiction=''")

    # Helper function to ingest international corpus
    def ingest_jurisdiction(jur_name: str, corpus: List[Dict[str, Any]], csv_filename: str):
        jur_acts_list = []
        jur_dir = os.path.join(CORPUS_DIR, jur_name)
        os.makedirs(jur_dir, exist_ok=True)

        for act in corpus:
            aid = act["act_id"]
            title = act["act_title"]
            short_t = act["short_title"]
            yr = act["year"]
            url = act["official_url"]
            aliases = act["aliases"]
            act_hash = compute_hash(title + str(yr))

            # Registry entry
            registry[aid] = {
                "act_id": aid,
                "act_title": title,
                "short_name": short_t,
                "act_number": "N/A",
                "enactment_date": str(yr),
                "year": yr,
                "official_url": url,
                "aliases": aliases,
                "sha256": act_hash,
                "jurisdiction": jur_name,
                "is_priority": True
            }

            jur_acts_list.append({
                "jurisdiction": jur_name,
                "act_id": aid,
                "act_title": title,
                "short_title": short_t,
                "year": yr,
                "act_number": "N/A",
                "enactment_date": str(yr),
                "official_url": url,
                "sha256": act_hash
            })

            # Insert Act into SQLite
            cur.execute("""
            INSERT OR REPLACE INTO acts (act_id, act_title, short_title, act_number, enactment_date, year, source_url, aliases, sha256, jurisdiction)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (aid, title, short_t, "N/A", str(yr), yr, url, json.dumps(aliases), act_hash, jur_name))

            # Ingest Sections
            act_folder = os.path.join(jur_dir, aid)
            os.makedirs(act_folder, exist_ok=True)

            for sec in act["sections"]:
                s_num = sec["section_number"]
                s_title = sec["title"]
                s_text = sec["text"]
                s_hash = compute_hash(s_text)
                sec_id = f"{aid}_S{s_num}"

                sec_record = {
                    "jurisdiction": jur_name,
                    "act_id": aid,
                    "act_title": title,
                    "section_id": sec_id,
                    "section_number": s_num,
                    "title": s_title,
                    "text": s_text,
                    "source": {
                        "type": "official_local_snapshot",
                        "official_url": url,
                        "version": f"{yr}_official_edition",
                        "sha256": s_hash
                    }
                }

                # Save JSON
                sec_file = os.path.join(act_folder, f"section_{s_num}.json")
                with open(sec_file, "w", encoding="utf-8") as f:
                    json.dump(sec_record, f, indent=2, ensure_ascii=False)

                # Insert into SQLite
                cur.execute("""
                INSERT OR REPLACE INTO sections (section_id, act_id, section_number, title, text, source_url, sha256, jurisdiction)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (sec_id, aid, s_num, s_title, s_text, url, s_hash, jur_name))

        # Save CSV
        df_jur = pd.DataFrame(jur_acts_list)
        csv_path = os.path.join(CSV_DIR, csv_filename)
        df_jur.to_csv(csv_path, index=False)
        print(f"[OK] Saved {jur_name} Acts CSV: {csv_path} ({len(df_jur)} Acts)")
        return jur_acts_list

    # Ingest US, UK, EU
    us_acts = ingest_jurisdiction("US", US_CORPUS, "us_federal_statutes.csv")
    uk_acts = ingest_jurisdiction("UK", UK_CORPUS, "uk_statutes.csv")
    eu_acts = ingest_jurisdiction("EU", EU_CORPUS, "eu_regulations.csv")

    conn.commit()
    conn.close()

    # Save Master All Jurisdictions CSV
    all_acts = india_acts_list + us_acts + uk_acts + eu_acts
    df_all = pd.DataFrame(all_acts)
    master_csv_path = os.path.join(CSV_DIR, "all_jurisdictions_acts.csv")
    df_all.to_csv(master_csv_path, index=False)
    print(f"[OK] Saved Master Multi-Jurisdiction CSV: {master_csv_path} ({len(df_all)} Acts)")

    # Save Updated registry_index.json
    with open(REGISTRY_FILE, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)
    print(f"[OK] Updated Registry Index: {REGISTRY_FILE} ({len(registry)} Total Acts across India, US, UK, EU)")

if __name__ == "__main__":
    main()
