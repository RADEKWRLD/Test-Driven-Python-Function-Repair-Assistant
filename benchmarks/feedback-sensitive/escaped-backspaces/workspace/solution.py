def erase_marked(text, marker="#", escape="\\"):
    """Apply unescaped backspaces after consuming escapes in a string.

    marker/escape must be distinct one-character strings or raise ValueError.
    A marker deletes the last output character if one exists. Escape quotes
    the next character literally, including itself/marker, and is removed.
    Keep unmatched trailing escape. Later markers can delete quoted characters.
    """
    if len(marker) != 1 or len(escape) != 1 or marker == escape:
        raise ValueError("marker and escape must be distinct single characters")
    result = []
    for index, char in enumerate(text):
        escaped = index > 0 and text[index - 1] == escape
        if char == escape and not escaped and index + 1 < len(text):
            continue
        if char == marker and not escaped:
            if result:
                result.pop()
        else:
            result.append(char)
    return "".join(result)
