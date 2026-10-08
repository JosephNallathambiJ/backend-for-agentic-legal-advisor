#!/usr/bin/env python3
"""
build_index.py - Offline Legal Corpus Builder and Indexer
Processes the downloaded Indian Central Acts into:
1. data/registry/registry_index.json (Registry metadata, official IDs/URLs, aliases)
2. data/legal_corpus/<ACT_ID>/ (Normalized JSON per section with sha256 hashes)
3. data/cache/legal_cache.sqlite (SQLite indexed database for zero-latency offline retrieval)
"""

import os
import sys
import json
import sqlite3
import hashlib
import re
import pandas as pd
from typing import Dict, List, Any

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARQUET_FILE = os.path.join(WORKSPACE_DIR, "indian_central_acts.parquet")
DATA_DIR = os.path.join(WORKSPACE_DIR, "data")
CORPUS_DIR = os.path.join(DATA_DIR, "legal_corpus")
CACHE_DIR = os.path.join(DATA_DIR, "cache")
REGISTRY_DIR = os.path.join(DATA_DIR, "registry")
REGISTRY_FILE = os.path.join(REGISTRY_DIR, "registry_index.json")
SQLITE_DB = os.path.join(CACHE_DIR, "legal_cache.sqlite")

# Canonical identifiers and aliases for priority acts
PRIORITY_ACTS = {
    "The Bharatiya Nyaya Sanhita, 2023": {
        "act_id": "BNS_2023",
        "short_name": "BNS",
        "year": 2023,
        "aliases": ["bns", "bharatiya nyaya sanhita", "bns 2023", "nyaya sanhita", "indian penal code replacement"]
    },
    "The Bharatiya Nagarik Suraksha Sanhita, 2023": {
        "act_id": "BNSS_2023",
        "short_name": "BNSS",
        "year": 2023,
        "aliases": ["bnss", "bharatiya nagarik suraksha sanhita", "bnss 2023", "nagarik suraksha", "crpc replacement"]
    },
    "The Bharatiya Sakshya Adhiniyam, 2023": {
        "act_id": "BSA_2023",
        "short_name": "BSA",
        "year": 2023,
        "aliases": ["bsa", "bharatiya sakshya adhiniyam", "bsa 2023", "sakshya adhiniyam", "evidence act replacement"]
    },
    "The Indian Contract Act, 1872": {
        "act_id": "ICA_1872",
        "short_name": "Contract Act",
        "year": 1872,
        "aliases": ["ica", "contract act", "indian contract act", "ica 1872", "contract act 1872"]
    },
    "The Code of Civil Procedure, 1908": {
        "act_id": "CPC_1908",
        "short_name": "CPC",
        "year": 1908,
        "aliases": ["cpc", "code of civil procedure", "cpc 1908", "civil procedure code"]
    },
    "The Arbitration and Conciliation Act, 1996": {
        "act_id": "ARBITRATION_1996",
        "short_name": "Arbitration Act",
        "year": 1996,
        "aliases": ["arbitration act", "arbitration and conciliation act", "arbitration 1996"]
    },
    "The Information Technology Act, 2000": {
        "act_id": "IT_2000",
        "short_name": "IT Act",
        "year": 2000,
        "aliases": ["it act", "information technology act", "it act 2000", "cyber law"]
    },
    "The Consumer Protection Act, 2019": {
        "act_id": "CONSUMER_2019",
        "short_name": "Consumer Act",
        "year": 2019,
        "aliases": ["consumer protection act", "copra", "consumer act 2019"]
    }
}

def compute_hash(text: str) -> str:
    return hashlib.sha256(text.strip().encode("utf-8")).hexdigest()

def normalize_text(text: str) -> str:
    text = re.sub(r"\r\n", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

def parse_sections_from_markdown(act_id: str, act_title: str, markdown: str, official_url: str) -> List[Dict[str, Any]]:
    """
    Extracts substantive sections from the act markdown.
    Skips the Arrangement of Sections / Table of Contents by finding substantive preamble/start.
    """
    sections = []
    
    # Locate where substantive text begins
    start_pos = 0
    substantive_anchors = [
        "This Act may be called",
        "ARRANGEMENT OF SECTIONS",
        "ARRANGEMENT OF CLAUSES",
        "PRELIMINARY"
    ]
    
    # Check if "This Act may be called" exists (usually Section 1 body)
    anchor_idx = markdown.find("This Act may be called")
    if anchor_idx != -1:
        # Step back to the start of section 1
        sec1_idx = markdown.rfind("\n1.", 0, anchor_idx)
        if sec1_idx != -1:
            start_pos = sec1_idx
        else:
            start_pos = max(0, anchor_idx - 100)
    else:
        # Fallback: after arrangement of sections
        arr_idx = markdown.find("ARRANGEMENT OF SECTIONS")
        if arr_idx != -1:
            # find next major heading or second section 1
            sec1_matches = list(re.finditer(r"\n1\.\s+[A-Z]", markdown))
            if len(sec1_matches) > 1:
                start_pos = sec1_matches[-1].start()
            else:
                start_pos = arr_idx + len("ARRANGEMENT OF SECTIONS")

    substantive_text = markdown[start_pos:]

    # Match section headings such as:
    # \n1. Short title...
    # \n303. Theft.—...
    # \n73. Compensation for loss...
    sec_pattern = re.compile(
        r"(?:\n\s*(?:###?\s*|\*\*)?([0-9]+[A-Z]?)\.\s+([^\n]+))",
        re.MULTILINE
    )
    
    matches = list(sec_pattern.finditer(substantive_text))
    
    for i, match in enumerate(matches):
        sec_num = match.group(1).strip()
        raw_title = match.group(2).strip("*_ \t")
        
        # Determine title vs text
        # If title ends with .— or contains dash, extract title and start of body
        title = raw_title
        if ".—" in raw_title:
            parts = raw_title.split(".—", 1)
            title = parts[0].strip()
        elif "—" in raw_title:
            parts = raw_title.split("—", 1)
            title = parts[0].strip()
        elif ". ––" in raw_title:
            parts = raw_title.split(". ––", 1)
            title = parts[0].strip()
        
        # Section span bounds
        sec_start = match.start()
        sec_end = matches[i + 1].start() if i + 1 < len(matches) else len(substantive_text)
        
        body_text = normalize_text(substantive_text[sec_start:sec_end])
        
        # Clean markdown formatting marks
        clean_text = re.sub(r"\[\d+\]", "", body_text) # remove footnote brackets
        clean_text = re.sub(r"\*+", "", clean_text)    # remove bold/italics markers
        clean_text = normalize_text(clean_text)
        
        if len(clean_text) < 15:
            continue

        sec_hash = compute_hash(clean_text)
        
        sections.append({
            "act_id": act_id,
            "act_title": act_title,
            "section_id": f"{act_id}_S{sec_num}",
            "section_number": sec_num,
            "title": title[:200],
            "text": clean_text,
            "source": {
                "type": "official_local_snapshot",
                "official_url": official_url,
                "version": "official_gazette_2023",
                "sha256": sec_hash
            }
        })
        
    return sections

def main():
    print(f"Loading {PARQUET_FILE}...")
    if not os.path.exists(PARQUET_FILE):
        print(f"Error: {PARQUET_FILE} not found. Run download_acts.py first.")
        sys.exit(1)
        
    df = pd.read_parquet(PARQUET_FILE)
    print(f"Total acts loaded: {len(df)}")
    
    os.makedirs(CORPUS_DIR, exist_ok=True)
    os.makedirs(CACHE_DIR, exist_ok=True)
    os.makedirs(REGISTRY_DIR, exist_ok=True)
    
    # Initialize SQLite database
    conn = sqlite3.connect(SQLITE_DB)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS acts (
        act_id TEXT PRIMARY KEY,
        act_title TEXT NOT NULL,
        short_title TEXT NOT NULL,
        act_number TEXT,
        enactment_date TEXT,
        year INTEGER,
        source_url TEXT,
        aliases TEXT,
        sha256 TEXT
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS sections (
        section_id TEXT PRIMARY KEY,
        act_id TEXT NOT NULL,
        section_number TEXT NOT NULL,
        title TEXT,
        text TEXT NOT NULL,
        source_url TEXT,
        sha256 TEXT,
        FOREIGN KEY (act_id) REFERENCES acts (act_id)
    )
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_sections_act_num ON sections(act_id, section_number)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_sections_text ON sections(text)")
    
    registry = {}
    total_sections_indexed = 0

    # 1. First register all 883 acts into registry
    for idx, row in df.iterrows():
        short_title = str(row.get("Short Title", "")).strip()
        act_num = str(row.get("Act Number", "")).strip()
        enact_date = str(row.get("Enactment Date", "")).strip()
        view_url = str(row.get("View", "")).strip()
        
        # Parse year from title or date
        year = None
        year_match = re.search(r"\b(18\d\d|19\d\d|20\d\d)\b", short_title)
        if year_match:
            year = int(year_match.group(1))
        elif enact_date:
            year_match = re.search(r"\b(18\d\d|19\d\d|20\d\d)\b", enact_date)
            if year_match:
                year = int(year_match.group(1))

        # Check if priority act
        matched_priority = None
        for p_title, p_meta in PRIORITY_ACTS.items():
            if p_title.lower() in short_title.lower() or short_title.lower() in p_title.lower():
                matched_priority = p_meta
                break
                
        if matched_priority:
            act_id = matched_priority["act_id"]
            short_name = matched_priority["short_name"]
            aliases = matched_priority["aliases"]
        else:
            # Generate deterministic act_id
            clean_name = re.sub(r"[^A-Za-z0-9]+", "_", short_title).strip("_")[:30].upper()
            act_id = f"ACT_{clean_name}_{year or 'UNDATED'}"
            short_name = short_title
            aliases = [short_title.lower()]

        act_hash = compute_hash(short_title + enact_date + act_num)
        
        # Add to registry
        registry[act_id] = {
            "act_id": act_id,
            "act_title": short_title,
            "short_name": short_name,
            "act_number": act_num,
            "enactment_date": enact_date,
            "year": year,
            "official_url": view_url,
            "aliases": aliases,
            "sha256": act_hash,
            "is_priority": matched_priority is not None
        }

        # Insert act into SQLite
        cur.execute("""
        INSERT OR REPLACE INTO acts (act_id, act_title, short_title, act_number, enactment_date, year, source_url, aliases, sha256)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (act_id, short_title, short_name, act_num, enact_date, year, view_url, json.dumps(aliases), act_hash))

    # 2. Extract and index sections for priority acts & all acts with substantial markdown
    for idx, row in df.iterrows():
        short_title = str(row.get("Short Title", "")).strip()
        markdown = str(row.get("Markdown", "")).strip()
        view_url = str(row.get("View", "")).strip()
        
        matched_priority = None
        for p_title, p_meta in PRIORITY_ACTS.items():
            if p_title.lower() in short_title.lower() or short_title.lower() in p_title.lower():
                matched_priority = p_meta
                break
                
        if not matched_priority and len(markdown) < 5000:
            continue
            
        act_id = matched_priority["act_id"] if matched_priority else None
        if not act_id:
            clean_name = re.sub(r"[^A-Za-z0-9]+", "_", short_title).strip("_")[:30].upper()
            act_id = f"ACT_{clean_name}_{registry.get(clean_name, {}).get('year', 'UNDATED')}"

        sections = parse_sections_from_markdown(act_id, short_title, markdown, view_url)
        if not sections:
            continue

        act_dir = os.path.join(CORPUS_DIR, act_id)
        os.makedirs(act_dir, exist_ok=True)
        
        for sec in sections:
            sec_num = sec["section_number"]
            # Save section json
            sec_file = os.path.join(act_dir, f"section_{sec_num}.json")
            with open(sec_file, "w", encoding="utf-8") as f:
                json.dump(sec, f, indent=2, ensure_ascii=False)
                
            # Insert into SQLite
            cur.execute("""
            INSERT OR REPLACE INTO sections (section_id, act_id, section_number, title, text, source_url, sha256)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (sec["section_id"], act_id, sec_num, sec["title"], sec["text"], view_url, sec["source"]["sha256"]))
            total_sections_indexed += 1

    conn.commit()
    conn.close()

    # Save registry_index.json
    with open(REGISTRY_FILE, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)

    print(f"Successfully created:")
    print(f" - Registry: {REGISTRY_FILE} ({len(registry)} Acts registered)")
    print(f" - SQLite Cache: {SQLITE_DB} ({total_sections_indexed} sections indexed)")
    print(f" - Priority Corpus directories created under {CORPUS_DIR}")

if __name__ == "__main__":
    main()
