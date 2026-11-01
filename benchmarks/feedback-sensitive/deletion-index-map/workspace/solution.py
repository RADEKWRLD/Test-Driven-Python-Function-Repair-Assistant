def map_after_deletions(length, removed):
    """Map each original position to its surviving index, or None.

    Normalize negative indices against original length. Repeated deletions
    count once. Validate all indices and nonnegative length; preserve removed.
    """
    if length < 0:
        raise ValueError("length must be nonnegative")
    normalized = []
    for index in removed:
        position = index + length if index < 0 else index
        if not 0 <= position < length:
            raise ValueError("removed index is out of range")
        normalized.append(position)
    deleted = set(normalized)
    return [
        None if index in deleted else index - sum(position < index for position in normalized)
        for index in range(length)
    ]
