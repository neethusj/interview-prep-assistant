import re

MAX_INPUT_LENGTH = 2000

# Patterns that commonly signal prompt injection attempts
SUSPICIOUS_PATTERNS = [
    r"ignore (all )?(previous|above|prior) instructions",
    r"system prompt",
    r"you are now",
    r"disregard (all )?(previous|above)",
    r"act as (if|a)",
    r"forget (everything|all|your instructions)",
    r"</?(system|assistant|user)>",
]

def sanitize_input(text: str) -> str:
    """
    Cleans and validates free-text user input before it reaches an LLM prompt.
    Strips length, removes suspicious injection patterns, and neutralizes
    any fake role/tag markers.
    """
    if not text:
        return ""

    # Trim to a safe max length
    text = text.strip()[:MAX_INPUT_LENGTH]

    # Remove/neutralize any HTML-like or role tags
    text = re.sub(r"<[^>]+>", "", text)

    # Flag and neutralize suspicious instruction-override phrases
    for pattern in SUSPICIOUS_PATTERNS:
        text = re.sub(pattern, "[filtered]", text, flags=re.IGNORECASE)

    return text


def is_suspicious(text: str) -> bool:
    """Returns True if input contains likely prompt-injection attempts."""
    if not text:
        return False
    for pattern in SUSPICIOUS_PATTERNS:
        if re.search(pattern, text, flags=re.IGNORECASE):
            return True
    return False