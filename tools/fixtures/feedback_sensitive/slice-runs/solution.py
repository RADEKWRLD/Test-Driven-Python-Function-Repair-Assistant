def slice_runs(runs, start, stop):
    """Author reference; never included in a model workspace."""
    total = 0
    for _value, count in runs:
        if count < 0:
            raise ValueError("run counts must be nonnegative")
        total += count
    lower, upper, _ = slice(start, stop).indices(total)
    result = []
    offset = 0
    for value, count in runs:
        left = max(lower, offset)
        right = min(upper, offset + count)
        if left < right:
            result.extend([value] * (right - left))
        offset += count
    return result
