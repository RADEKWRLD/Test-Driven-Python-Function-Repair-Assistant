from collections import Counter


def sliding_modes(items, width):
    """Return each full window's mode, breaking ties toward the smallest value."""
    if width <= 0:
        raise ValueError("width must be positive")

    counts = Counter()
    result = []
    for index, value in enumerate(items):
        counts[value] += 1
        if index >= width:
            outgoing = items[index - width]
            if counts[outgoing] > 1:
                counts[outgoing] -= 1
        if index + 1 >= width:
            result.append(min(counts, key=lambda item: (-counts[item], item)))

    return result
