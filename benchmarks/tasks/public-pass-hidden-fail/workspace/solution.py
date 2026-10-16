def normalize_whitespace(text: str) -> str:
    """Normalize whitespace between words."""
    return " ".join(text.strip().split(" "))
