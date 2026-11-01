def tokenize_quoted(text):
    """Split string whitespace outside double quotes, removing double quotes.

    Use str.isspace(). Adjacent quoted/unquoted fragments concatenate. Keep
    empty quoted tokens and quoted whitespace. Backslashes/single quotes are
    literal; no escape syntax exists. Unmatched double quotes raise ValueError.
    Empty or unquoted-whitespace-only input returns [].
    """
    tokens = []
    current = []
    quoted = False
    for char in text:
        if char == '"':
            quoted = not quoted
        elif char.isspace() and not quoted:
            if current:
                tokens.append("".join(current))
                current = []
        else:
            current.append(char)
    if quoted:
        raise ValueError("unmatched double quote")
    if current:
        tokens.append("".join(current))
    return tokens
