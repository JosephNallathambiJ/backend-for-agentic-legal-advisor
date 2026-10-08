"""
core/logging_config.py - Structured logging with PII redaction
"""

import logging
import re
import json
from typing import Any

# Patterns to redact in logs (PAN, Phone, Aadhaar, Email)
REDACT_PATTERNS = [
    (re.compile(r"\b[A-Z]{5}[0-9]{4}[A-Z]\b"), "[REDACTED_PAN]"),
    (re.compile(r"\b(?:\+91[\-\s]?)?[6-9]\d{9}\b"), "[REDACTED_PHONE]"),
    (re.compile(r"\b\d{4}\s\d{4}\s\d{4}\b"), "[REDACTED_AADHAAR]"),
    (re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"), "[REDACTED_EMAIL]"),
]

class RedactingFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        msg = super().format(record)
        for pattern, replacement in REDACT_PATTERNS:
            msg = pattern.sub(replacement, msg)
        return msg

def setup_logger(name: str = "legal_assistant", level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(level)
        handler = logging.StreamHandler()
        formatter = RedactingFormatter(
            fmt="[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

logger = setup_logger()
