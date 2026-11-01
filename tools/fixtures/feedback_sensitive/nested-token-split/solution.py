def split_top_level(text, delimiter=","):
    if len(delimiter) != 1 or delimiter in "()":
        raise ValueError("delimiter must be one non-parenthesis character")
    depth = 0
    fields = []
    start = 0
    for index, char in enumerate(text):
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth < 0:
                raise ValueError("unmatched closing parenthesis")
        elif char == delimiter and depth == 0:
            fields.append(text[start:index])
            start = index + 1
    if depth:
        raise ValueError("unmatched opening parenthesis")
    fields.append(text[start:])
    return fields
