#!/usr/bin/env bash
# scripts/setup_models.sh - Offline Model & Resource Verification
# STRICT RULE: Makes ZERO network calls, zero curl/wget/pip/huggingface_hub downloads.
# Inspects local directories, reports status, and fails closed if mandatory components are absent.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"

echo "============================================================"
echo " OFFLINE MODEL & RESOURCE PRE-FLIGHT AUDIT"
echo " (Strict Offline Verification - 0 Outbound Requests)"
echo "============================================================"

LLM_DIR="${BASE_DIR}/models/llm"
ASR_DIR="${BASE_DIR}/models/asr"
NLI_DIR="${BASE_DIR}/models/nli"
TTS_DIR="${BASE_DIR}/models/tts"
DATA_DIR="${BASE_DIR}/data"

EXIT_CODE=0

# 1. Check Legal Corpus & Registry
echo -n "[CHECK] Legal Corpus Registry: "
if [ -f "${DATA_DIR}/registry/registry_index.json" ]; then
    echo "[OK] Found ($(jq 'keys | length' "${DATA_DIR}/registry/registry_index.json" 2>/dev/null || echo "indexed") acts)"
else
    echo "[FAIL] data/registry/registry_index.json MISSING"
    EXIT_CODE=1
fi

echo -n "[CHECK] SQLite Legal Cache: "
if [ -f "${DATA_DIR}/cache/legal_cache.sqlite" ]; then
    echo "[OK] Found (${DATA_DIR}/cache/legal_cache.sqlite)"
else
    echo "[FAIL] data/cache/legal_cache.sqlite MISSING"
    EXIT_CODE=1
fi

# 2. Check LLM GGUF
echo -n "[CHECK] Local LLM GGUF: "
GGUF_COUNT=$(find "${LLM_DIR}" -name "*.gguf" 2>/dev/null | wc -l)
if [ "${GGUF_COUNT}" -gt 0 ]; then
    MODEL_PATH=$(find "${LLM_DIR}" -name "*.gguf" 2>/dev/null | head -n 1)
    echo "[OK] Found GGUF: ${MODEL_PATH}"
else
    echo "[INFO] No .gguf found in models/llm/."
    echo "       -> Defaulting to local deterministic rule-based drafting engine."
    echo "       -> To enable neural GGUF: place 'qwen2.5-1.5b-instruct-q4_k_m.gguf' in models/llm/"
fi

# 3. Check ASR
echo -n "[CHECK] Local ASR (Whisper): "
ASR_COUNT=$(find "${ASR_DIR}" -type f 2>/dev/null | wc -l)
if [ "${ASR_COUNT}" -gt 0 ]; then
    echo "[OK] Found local ASR files in ${ASR_DIR}"
else
    echo "[INFO] Voice ASR disabled/unprovisioned. Text pipeline is primary."
fi

# 4. Check NLI
echo -n "[CHECK] Local NLI: "
NLI_COUNT=$(find "${NLI_DIR}" -type f 2>/dev/null | wc -l)
if [ "${NLI_COUNT}" -gt 0 ]; then
    echo "[OK] Found local NLI weights in ${NLI_DIR}"
else
    echo "[INFO] Using deterministic calibrated local NLI alignment gate."
fi

# 5. Check TTS
echo -n "[CHECK] Local TTS: "
TTS_COUNT=$(find "${TTS_DIR}" -type f 2>/dev/null | wc -l)
if [ "${TTS_COUNT}" -gt 0 ]; then
    echo "[OK] Found local TTS weights in ${TTS_DIR}"
else
    echo "[INFO] Local TTS disabled/unprovisioned."
fi

echo "============================================================"
if [ "${EXIT_CODE}" -eq 0 ]; then
    echo "Pre-flight audit PASSED. System is ready for OFFLINE operation."
else
    echo "Pre-flight audit FAILED. Mandatory local files missing."
fi
echo "============================================================"

exit ${EXIT_CODE}
