def merge_intervals(intervals):
    """Return the union of valid nonempty half-open integer intervals.

    Merge touching endpoints as well as overlaps. Validate every interval,
    ignore empty intervals, preserve input, and return sorted tuples.
    """
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
            merged[-1] = (merged[-1][0], end)
    return merged
