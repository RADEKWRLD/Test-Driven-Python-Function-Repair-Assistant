def merge_intervals(intervals):
    """Author reference; never included in a model workspace."""
    ordered = []
    for start, end in intervals:
        if end < start:
            raise ValueError("end must not precede start")
        if start < end:
            ordered.append((start, end))
    ordered.sort()
    merged = []
    for start, end in ordered:
        if not merged or start > merged[-1][1]:
            merged.append((start, end))
        else:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
    return merged
