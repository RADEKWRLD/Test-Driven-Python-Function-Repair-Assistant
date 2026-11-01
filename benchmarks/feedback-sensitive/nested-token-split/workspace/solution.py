def split_top_level(text, delimiter=","):
    """Split at depth-zero delimiters, preserving parentheses and empty fields.

    Strings only. Delimiter is one character other than '(' or ')'; invalid
    delimiters and unmatched parentheses raise ValueError. Quotes/backslashes
    have no special meaning. Empty input yields [""]. Preserve the signature.
    """
    if len(delimiter) != 1 or delimiter in "()":
        raise ValueError("delimiter must be one non-parenthesis character")
    balance = 0
    inside = False
    fields = []
    start = 0
    for index, char in enumerate(text):
        if char == "(":
            balance += 1
            inside = True
        elif char == ")":
            balance -= 1
            if balance < 0:
                raise ValueError("unmatched closing parenthesis")
            inside = False
        elif char == delimiter and not inside:
            fields.append(text[start:index])
            start = index + 1
    if balance:
        raise ValueError("unmatched opening parenthesis")
    fields.append(text[start:])
    return fields
