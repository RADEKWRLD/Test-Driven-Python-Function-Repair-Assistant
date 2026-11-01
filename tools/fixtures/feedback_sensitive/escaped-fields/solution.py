def split_escaped(text, delimiter=",", escape="\\"):
    if len(delimiter) != 1 or len(escape) != 1 or delimiter == escape:
        raise ValueError("delimiter and escape must be distinct single characters")
    fields = []
    current = []
    index = 0
    while index < len(text):
        char = text[index]
        if char == escape and index + 1 < len(text):
            index += 1
            current.append(text[index])
        elif char == delimiter:
            fields.append("".join(current))
            current = []
        else:
            current.append(char)
        index += 1
    fields.append("".join(current))
    return fields
