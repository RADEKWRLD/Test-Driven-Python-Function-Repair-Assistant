def round_robin_drain(rows):
    """Reference implementation; never copy this file into the model workspace."""
    active = [(row, 0) for row in rows if row]
    result = []
    cursor = 0

    while active:
        row, offset = active[cursor]
        result.append(row[offset])
        offset += 1

        if offset == len(row):
            active.pop(cursor)
        else:
            active[cursor] = (row, offset)
            cursor += 1

        if cursor >= len(active):
            cursor = 0

    return result
