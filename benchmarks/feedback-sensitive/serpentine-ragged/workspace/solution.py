def serpentine_ragged(rows):
    """Flatten rows, reversing every second nonempty row without mutation.

    Empty rows do not contribute elements or change the next direction.
    """
    result = []
    reverse = False

    for row in rows:
        if row:
            values = list(row)
            if reverse:
                values.reverse()
            result.extend(values)
        reverse = not reverse

    return result
