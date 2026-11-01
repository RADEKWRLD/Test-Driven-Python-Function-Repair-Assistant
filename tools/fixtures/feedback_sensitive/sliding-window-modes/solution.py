from collections import Counter


def sliding_modes(items, width):
    """Reference implementation; keep outside the model workspace."""
    if width <= 0:
        raise ValueError("width must be positive")

    counts = Counter()
    result = []
    for index, value in enumerate(items):
        counts[value] += 1
        if index >= width:
            outgoing = items[index - width]
            counts[outgoing] -= 1
            if counts[outgoing] == 0:
                del counts[outgoing]
        if index + 1 >= width:
            result.append(min(counts, key=lambda item: (-counts[item], item)))

    return result
