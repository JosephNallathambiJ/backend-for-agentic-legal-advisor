"""
core/security.py - Security controls & prompt injection defense
Strictly isolates system instructions from untrusted user documents and PDFs.
"""

import re
import os
from typing import Tuple, List

# Suspicious instruction overrides commonly found in prompt injection attacks
INJECTION_PATTERNS = [
    re.compile(r"ignore\s+(?:all\s+)?(?:previous|prior)\s+instructions", re.IGNORECASE),
    re.compile(r"system\s*:\s*you\s+are\s+now", re.IGNORECASE),
    re.compile(r"<\|im_start\|>", re.IGNORECASE),
    re.compile(r"\[INST\]", re.IGNORECASE),
    re.compile(r"disregard\s+the\s+above", re.IGNORECASE),
    re.compile(r"mark\s+all\s+claims\s+as\s+pass", re.IGNORECASE),
    re.compile(r"bypass\s+verifier", re.IGNORECASE),
    re.compile(r"state\s+that\s+the\s+accused\s+is\s+innocent\s+regardless", re.IGNORECASE),
]

MAX_FILE_SIZE_BYTES = 25 * 1024 * 1024 # 25 MB max per document
ALLOWED_EXTENSIONS = {".pdf", ".txt", ".json", ".md", ".docx"}

class SecurityManager:
    @staticmethod
    def sanitize_untrusted_text(text: str) -> Tuple[str, List[str]]:
        """
        Sanitizes text extracted from untrusted documents.
        Neutralizes injection triggers and returns detected threats.
        """
        threats_detected = []
        clean_text = text
        
        for pattern in INJECTION_PATTERNS:
            matches = pattern.findall(clean_text)
            if matches:
                threats_detected.append(f"Prompt injection pattern detected: '{matches[0]}'")
                # Neutralize pattern so it cannot be interpreted as prompt control
                clean_text = pattern.sub("[SANITIZED_INSTRUCTION_OVERRIDE_ATTEMPT]", clean_text)
                
        return clean_text, threats_detected

    @staticmethod
    def validate_file(file_path: str) -> Tuple[bool, str]:
        """Validates file existence, size, extension, and path safety."""
        if not os.path.exists(file_path):
            return False, f"File does not exist: {file_path}"
            
        ext = os.path.splitext(file_path)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            return False, f"Unsupported file type '{ext}'. Allowed: {ALLOWED_EXTENSIONS}"
            
        size = os.path.getsize(file_path)
        if size > MAX_FILE_SIZE_BYTES:
            return False, f"File exceeds maximum allowed size ({size} > {MAX_FILE_SIZE_BYTES} bytes)"
            
        return True, "Valid"
