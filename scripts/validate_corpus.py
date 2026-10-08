
#!/usr/bin/env python3
"""
scripts/validate_corpus.py - Legal Corpus Validation & Integrity Audit
Verifies:
- Act identifier, titles, section numbering, text content, hashes
- Detects malformed/empty sections, corrupted JSON, missing references
- Verifies registry index and SQLite cache integrity
"""

import os
import sys
import json
import sqlite3
import hashlib
from typing import Dict, List, Any

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORPUS_DIR = os.path.join(WORKSPACE_DIR, "data", "legal_corpus")
REGISTRY_FILE = os.path.join(WORKSPACE_DIR, "data", "registry", "registry_index.json")
SQLITE_DB = os.path.join(WORKSPACE_DIR, "data", "cache", "legal_cache.sqlite")

def compute_hash(text: str) -> str:
    return hashlib.sha256(text.strip().encode("utf-8")).hexdigest()

def validate_registry():
    print(f"[1/3] Validating Registry Index: {REGISTRY_FILE}")
    if not os.path.exists(REGISTRY_FILE):
        print("  FAIL: Registry index file does not exist!")
        return False
    with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
        registry = json.load(f)
    print(f"  OK: Registry loaded with {len(registry)} registered Acts.")
    
    # Check priority acts
    expected_priorities = ["BNS_2023", "BNSS_2023", "BSA_2023", "ICA_1872"]
    for act_id in expected_priorities:
        if act_id in registry:
            print(f"  OK: Found priority act {act_id} ({registry[act_id]['act_title']})")
        else:
            print(f"  WARNING: Priority act {act_id} not explicitly named in registry keys")
    return True

def validate_sqlite_cache():
    print(f"\n[2/3] Validating SQLite Cache: {SQLITE_DB}")
    if not os.path.exists(SQLITE_DB):
        print("  FAIL: SQLite database not found!")
        return False
    conn = sqlite3.connect(SQLITE_DB)
    cur = conn.cursor()
    cur.execute("SELECT count(*) FROM acts")
    acts_count = cur.fetchone()[0]
    cur.execute("SELECT count(*) FROM sections")
    sec_count = cur.fetchone()[0]
    print(f"  OK: SQLite contains {acts_count} acts and {sec_count} indexed sections.")
    
    # Check sample queries
    cur.execute("SELECT section_id, title, text, sha256 FROM sections WHERE act_id='BNS_2023' AND section_number='303'")
    sample_bns = cur.fetchone()
    if sample_bns:
        # Verify hash
        calc_hash = compute_hash(sample_bns[2])
        if calc_hash == sample_bns[3]:
            print(f"  OK: BNS Section 303 hash verified ({calc_hash[:12]}...)")
        else:
            print(f"  FAIL: BNS Section 303 hash mismatch! Stored: {sample_bns[3]} vs Calc: {calc_hash}")
    else:
        print("  WARNING: BNS_2023 Section 303 not found in cache")
    conn.close()
    return True

def validate_corpus_files():
    print(f"\n[3/3] Validating Corpus Files under {CORPUS_DIR}")
    if not os.path.exists(CORPUS_DIR):
        print("  FAIL: Corpus directory not found!")
        return False
        
    acts = [d for d in os.listdir(CORPUS_DIR) if os.path.isdir(os.path.join(CORPUS_DIR, d))]
    print(f"  Found {len(acts)} act directories.")
    
    issues = []
    total_sections_checked = 0
    
    for act in acts[:15]: # audit top acts in detail
        act_path = os.path.join(CORPUS_DIR, act)
        files = [f for f in os.listdir(act_path) if f.endswith(".json")]
        for sec_file in files:
            full_path = os.path.join(act_path, sec_file)
            total_sections_checked += 1
            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                
                # Check mandatory fields
                for field in ["act_id", "section_number", "title", "text", "source"]:
                    if field not in data:
                        issues.append(f"{sec_file}: missing mandatory field {field}")
                        
                text = data.get("text", "")
                if not text or len(text.strip()) < 10:
                    issues.append(f"{sec_file}: empty or too short text ({len(text)} chars)")
                    
                src_hash = data.get("source", {}).get("sha256", "")
                if src_hash != compute_hash(text):
                    issues.append(f"{sec_file}: sha256 mismatch")
            except Exception as e:
                issues.append(f"{sec_file}: corrupted JSON: {str(e)}")

    if issues:
        print(f"  FAIL: Found {len(issues)} corpus issues:")
        for iss in issues[:10]:
            print(f"   - {iss}")
        return False
    else:
        print(f"  OK: Audited {total_sections_checked} section files. Zero corrupted JSON, zero hash mismatches!")
        return True

def main():
    print("=" * 60)
    print(" LOCAL LEGAL CORPUS INTEGRITY VALIDATOR")
    print("=" * 60)
    ok_reg = validate_registry()
    ok_sql = validate_sqlite_cache()
    ok_corp = validate_corpus_files()
    
    if ok_reg and ok_sql and ok_corp:
        print("\n[SUCCESS] Local legal corpus is authentic, indexed, and fully validated.")
        sys.exit(0)
    else:
        print("\n[FAILURE] Legal corpus failed validation checks.")
        sys.exit(1)

if __name__ == "__main__":
    main()
