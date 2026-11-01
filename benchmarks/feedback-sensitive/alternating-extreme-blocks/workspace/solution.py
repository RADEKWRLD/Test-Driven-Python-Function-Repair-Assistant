def alternating_extreme_blocks(items, block_size):
    """Consume sorted extremes in alternating low/high blocks without mutation."""
    if block_size <= 0:
        raise ValueError("block_size must be positive")

    ordered = sorted(items)
    result = []
    left = 0
    right = len(ordered)

    while left < right:
        count = min(block_size, right - left)
        take_low = len(result) % 2 == 0
        if take_low:
            result.extend(ordered[left:left + count])
            left += count
        else:
            result.extend(reversed(ordered[right - count:right]))
            right -= count

    return result
