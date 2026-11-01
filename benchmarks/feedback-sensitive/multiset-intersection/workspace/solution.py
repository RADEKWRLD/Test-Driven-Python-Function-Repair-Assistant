from collections import Counter


def multiset_intersection(left, right):
    """Return shared occurrences in left-input order without mutating inputs."""
    remaining = Counter(right)
    result = []

    for value in left:
        if remaining.get(value, 0) > 0:
            result.append(value)
            remaining.pop(value)

    return result
