def cap_runs(items, limit):
    if limit < 0:
        raise ValueError("limit must be nonnegative")
    result = []
    have_previous = False
    previous = None
    count = 0
    for item in items:
        if have_previous and item == previous:
            count += 1
        else:
            count = 1
        if count <= limit:
            result.append(item)
        previous = item
        have_previous = True
    return result
