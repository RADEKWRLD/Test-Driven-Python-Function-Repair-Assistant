from collections import Counter


def multiset_intersection(left, right):
    """Reference implementation; keep outside the model workspace."""
    remaining = Counter(right)
    result = []

    for value in left:
        if remaining.get(value, 0) > 0:
            result.append(value)
            remaining[value] -= 1

    return result
