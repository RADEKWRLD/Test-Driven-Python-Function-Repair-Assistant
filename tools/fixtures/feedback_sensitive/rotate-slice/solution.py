def rotate_slice(items, start, stop, steps):
    """Reference implementation; keep outside the model workspace."""
    result = list(items)
    left, right, _ = slice(start, stop).indices(len(result))
    selected = result[left:right]

    if not selected:
        return result

    shift = steps % len(selected)
    if shift:
        selected = selected[-shift:] + selected[:-shift]

    result[left:right] = selected
    return result
