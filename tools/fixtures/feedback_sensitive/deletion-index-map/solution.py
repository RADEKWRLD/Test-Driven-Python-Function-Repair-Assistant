def map_after_deletions(length, removed):
    """Author reference; never included in a model workspace."""
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
        None if index in deleted else index - sum(position < index for position in deleted)
        for index in range(length)
    ]
