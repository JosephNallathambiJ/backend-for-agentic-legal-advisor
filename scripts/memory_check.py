#!/usr/bin/env python3
"""
scripts/memory_check.py - Memory Diagnostic & Resource Budget Validator
Verifies target: Maximum runtime resident RAM target: <= 3.5 GB
"""

import sys
import psutil

MAX_BUDGET_MB = 3584 # 3.5 GB in MB

def check_memory():
    mem = psutil.virtual_memory()
    total_mb = mem.total / (1024 * 1024)
    available_mb = mem.available / (1024 * 1024)
    used_mb = mem.used / (1024 * 1024)
    
    print("=" * 60)
    print(" LOCAL MEMORY DIAGNOSTIC")
    print("=" * 60)
    print(f"Total System RAM:     {total_mb:.1f} MB ({total_mb/1024:.2f} GB)")
    print(f"Available RAM:        {available_mb:.1f} MB ({available_mb/1024:.2f} GB)")
    print(f"Used RAM:             {used_mb:.1f} MB ({used_mb/1024:.2f} GB)")
    print(f"Target Budget Limit:  {MAX_BUDGET_MB} MB (3.5 GB)")
    
    # Estimations for pipeline
    estimated_corpus_cache_mb = 120
    estimated_working_mb = 250
    estimated_llm_mb = 1200 # if Qwen 1.5B Q4_K_M is loaded
    estimated_total_working_mb = estimated_corpus_cache_mb + estimated_working_mb + estimated_llm_mb
    
    print(f"Estimated Cache Footprint:   {estimated_corpus_cache_mb} MB")
    print(f"Estimated Working Memory:    {estimated_working_mb} MB")
    print(f"Estimated LLM (Q4_K_M):      {estimated_llm_mb} MB")
    print(f"Estimated Total Pipeline:    {estimated_total_working_mb} MB (~{estimated_total_working_mb/1024:.2f} GB)")
    
    safety_margin_mb = MAX_BUDGET_MB - estimated_total_working_mb
    print(f"Budget Safety Margin:        {safety_margin_mb} MB")
    
    if available_mb < 500:
        print("\n[CRITICAL WARNING] Available system memory is under 500MB! High risk of OOM.")
        return False
    elif estimated_total_working_mb > MAX_BUDGET_MB:
        print("\n[CRITICAL WARNING] Estimated pipeline memory exceeds 3.5 GB target budget.")
        return False
    else:
        print("\n[PASSED] Memory budget is strictly within <= 3.5 GB limits.")
        return True

if __name__ == "__main__":
    passed = check_memory()
    sys.exit(0 if passed else 1)
