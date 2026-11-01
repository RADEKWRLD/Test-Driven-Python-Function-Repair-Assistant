def subtract_interval(interval, cuts):
    """Author reference; never included in a model workspace."""
    start, end = interval
    if end < start:
        raise ValueError("source end must not precede start")
    clipped = []
    for cut_start, cut_end in cuts:
        if cut_end < cut_start:
            raise ValueError("cut end must not precede start")
        left = max(start, cut_start)
        right = min(end, cut_end)
        if left < right:
            clipped.append((left, right))
    cursor = start
    remaining = []
    for cut_start, cut_end in sorted(clipped):
        if cut_start > cursor:
            remaining.append((cursor, cut_start))
        cursor = max(cursor, cut_end)
    if cursor < end:
        remaining.append((cursor, end))
    return remaining
