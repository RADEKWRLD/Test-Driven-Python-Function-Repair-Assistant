def slice_runs(runs, start, stop):
    """Return a unit-step slice of logically expanded run-length pairs.

    Normalize integer indices against expanded length, validate every count,
    and allocate only selected values. Never mutate input pairs or their list.
    """
    total = 0
    for value, count in runs:
        if count < 0:
            raise ValueError("run counts must be nonnegative")
        total += count
    lower, upper, _ = slice(start, stop).indices(len(runs))
    result = []
    offset = 0
    for value, count in runs:
        left = max(lower, offset)
        right = min(upper, offset + count)
        if left < right:
            result.extend([value] * (right - left))
        offset += count
    return result
