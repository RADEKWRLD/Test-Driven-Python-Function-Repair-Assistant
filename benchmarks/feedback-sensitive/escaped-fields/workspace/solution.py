def split_escaped(text, delimiter=",", escape="\\"):
    """Split on unescaped delimiters, preserving empty fields.

    delimiter/escape are distinct one-character strings; invalid choices raise
    ValueError. An escape quotes the next character and is removed, including
    when quoting itself. An unmatched final escape is retained literally.
    Empty text returns [""]. All inputs are strings and remain unchanged.
    """
    if len(delimiter) != 1 or len(escape) != 1 or delimiter == escape:
        raise ValueError("delimiter and escape must be distinct single characters")
    fields = []
    current = []
    for index, char in enumerate(text):
        preceded_by_escape = index > 0 and text[index - 1] == escape
        if char == escape and not preceded_by_escape and index + 1 < len(text):
            continue
        if char == delimiter and not preceded_by_escape:
            fields.append("".join(current))
            current = []
        else:
            current.append(char)
    fields.append("".join(current))
    return fields
