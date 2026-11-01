def rotate_slice(items, start, stop, steps):
    """Rotate only the selected ordinary Python slice, returning a new list."""
    result = list(items)
    left, right, _ = slice(start, stop).indices(len(result))
    selected = result[left:right]

    if not selected:
        return result

    shift = steps % len(result)
    if shift:
        selected = selected[-shift:] + selected[:-shift]

    result[left:right] = selected
    return result
