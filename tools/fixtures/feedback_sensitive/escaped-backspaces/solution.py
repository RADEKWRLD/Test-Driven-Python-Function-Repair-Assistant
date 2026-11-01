def erase_marked(text, marker="#", escape="\\"):
    if len(marker) != 1 or len(escape) != 1 or marker == escape:
        raise ValueError("marker and escape must be distinct single characters")
    result = []
    index = 0
    while index < len(text):
        char = text[index]
        if char == escape and index + 1 < len(text):
            index += 1
            result.append(text[index])
        elif char == marker:
            if result:
                result.pop()
        else:
            result.append(char)
        index += 1
    return "".join(result)
