import re

# Blocked keywords (PII, toxicity, jailbreak)
BLOCKED_PATTERNS = [
    r'\b\d{10}\b',  # Phone number
    r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Email
    r'\b[A-Z]{5,}\b',  # Random caps (jailbreak attempts)
    r'(ignore|bypass|jailbreak|system prompt|developer mode)',  # Prompt injection
]

def check_safety(text: str) -> bool:
    """Returns True if safe, False if blocked"""
    text_lower = text.lower()
    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, text_lower):
            return False
    return True