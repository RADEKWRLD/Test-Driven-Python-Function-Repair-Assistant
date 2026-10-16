def chunk_list(items: list[object], size: int) -> list[list[object]]:
    """Split items into consecutive chunks."""
    return [items[index : index + size] for index in range(0, len(items) - 1, size)]
