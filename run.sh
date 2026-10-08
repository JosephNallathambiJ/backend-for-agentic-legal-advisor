#!/usr/bin/env bash
# run.sh - Local Offline Backend Launch Script
# Pure headless backend service with strictly 0 outbound network calls (air-gapped local execution).

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${SCRIPT_DIR}"

# Select Python environment
if [ -d "${HOME}/legal_env" ]; then
    PYTHON_BIN="${HOME}/legal_env/bin/python"
elif [ -d "./venv" ]; then
    PYTHON_BIN="./venv/bin/python"
else
    PYTHON_BIN="python3"
fi

echo "============================================================"
echo " AGENTIC LEGAL ASSISTANT (PURE BACKEND)"
echo " Deterministic Verification Architecture (Offline Local)"
echo "============================================================"

# Step 1: Pre-flight model & corpus audit
./scripts/setup_models.sh

# Step 2: Memory check
${PYTHON_BIN} ./scripts/memory_check.py

# Step 3: Validate corpus integrity
${PYTHON_BIN} ./scripts/validate_corpus.py

# Step 4: Launch local backend REST API
echo ""
echo "[STARTING] Launching local backend REST API on http://127.0.0.1:8000"
echo "  - API Health:    http://127.0.0.1:8000/health"
echo "  - API Docs:      http://127.0.0.1:8000/docs"
echo "  - Run Pipeline:  POST http://127.0.0.1:8000/api/run"
echo "  - CLI Tool:      python cli.py --help"
echo "Press Ctrl+C to terminate."
echo "============================================================"

${PYTHON_BIN} -m uvicorn api.app:app --host 127.0.0.1 --port 8000 --log-level info
