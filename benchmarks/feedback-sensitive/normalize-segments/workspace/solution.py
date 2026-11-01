def normalize_segments(path):
    """Normalize a string path lexically using '/' only, with no filesystem IO.

    Ignore repeated '/' and '.'. '..' cancels an ordinary preceding segment,
    never another '..'. Preserve unresolved parents in relative paths; clamp
    absolute paths at root. Other names, spaces and backslashes are literal.
    Remove trailing slash except root. Empty results are '/' (absolute) or '.'.
    """
    absolute = path.startswith("/")
    segments = []
    for segment in path.split("/"):
        if segment in ("", "."):
            continue
        if segment == "..":
            if segments:
                segments.pop()
            elif not absolute:
                segments.append("..")
        else:
            segments.append(segment)
    normalized = ("/" if absolute else "") + "/".join(segments)
    return normalized or ("/" if absolute else ".")
