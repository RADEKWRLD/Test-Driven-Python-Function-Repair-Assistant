def alternating_extreme_blocks(items, block_size):
    """Reference implementation; never copy this file into the model workspace."""
    if block_size <= 0:
        raise ValueError("block_size must be positive")

    ordered = sorted(items)
    result = []
    left = 0
    right = len(ordered)
    take_low = True

    while left < right:
        count = min(block_size, right - left)
        if take_low:
            result.extend(ordered[left : left + count])
            left += count
        else:
            result.extend(reversed(ordered[right - count : right]))
            right -= count
        take_low = not take_low

    return result
