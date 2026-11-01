def wildcard_match(text, pattern):
    rows = len(text) + 1
    cols = len(pattern) + 1
    matched = [[False] * cols for _ in range(rows)]
    matched[0][0] = True
    for column in range(1, cols):
        if pattern[column - 1] == "*":
            matched[0][column] = matched[0][column - 1]
    for row in range(1, rows):
        for column in range(1, cols):
            token = pattern[column - 1]
            if token == "*":
                matched[row][column] = matched[row][column - 1] or matched[row - 1][column]
            elif token == "?" or token == text[row - 1]:
                matched[row][column] = matched[row - 1][column - 1]
    return matched[-1][-1]
