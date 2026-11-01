from collections import Counter


def count_bounded_sums(items, target, max_length):
    """Count nonempty matching-sum intervals within an inclusive length limit."""
    if max_length <= 0:
        raise ValueError("max_length must be positive")

    prefixes = [0]
    counts = Counter({0: 1})
    prefix = 0
    total = 0

    for end, value in enumerate(items, start=1):
        prefix += value
        expired = end - max_length
        if expired >= 0:
            previous = prefixes[expired]
            counts[previous] -= 1
            if counts[previous] == 0:
                del counts[previous]
        total += counts.get(prefix - target, 0)
        prefixes.append(prefix)
        counts[prefix] += 1

    return total
