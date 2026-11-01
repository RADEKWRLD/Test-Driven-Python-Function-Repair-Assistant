def tokenize_quoted(text):
    tokens = []
    current = []
    quoted = False
    active = False
    for char in text:
        if char == '"':
            quoted = not quoted
            active = True
        elif char.isspace() and not quoted:
            if active:
                tokens.append("".join(current))
                current = []
                active = False
        else:
            current.append(char)
            active = True
    if quoted:
        raise ValueError("unmatched double quote")
    if active:
        tokens.append("".join(current))
    return tokens
