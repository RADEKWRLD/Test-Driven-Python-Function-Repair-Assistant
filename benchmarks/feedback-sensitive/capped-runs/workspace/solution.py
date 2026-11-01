def cap_runs(items, limit):
    """Keep the first at most limit values of each consecutive equality run.

    Compare with Python ==: False/0 and True/1 are equal. Values may include
    None, booleans, numbers, strings and lists with scalar-valued equality.
    A repeated value after another run gets a new allowance. Preserve retained
    values and order; return a new list without mutating inputs or elements.
    limit is an integer: negative raises ValueError; zero yields [].
    """
    if limit < 0:
        raise ValueError("limit must be nonnegative")
    result = []
    values = []
    counts = []
    for item in items:
        for index, value in enumerate(values):
            if item == value:
                break
        else:
            index = len(values)
            values.append(item)
            counts.append(0)
        if counts[index] < limit:
            result.append(item)
            counts[index] += 1
    return result
