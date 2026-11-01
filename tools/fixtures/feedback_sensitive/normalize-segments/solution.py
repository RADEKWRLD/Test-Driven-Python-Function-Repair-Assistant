def normalize_segments(path):
    absolute = path.startswith("/")
    segments = []
    for segment in path.split("/"):
        if segment in ("", "."):
            continue
        if segment == "..":
            if segments and segments[-1] != "..":
                segments.pop()
            elif not absolute:
                segments.append("..")
        else:
            segments.append(segment)
    normalized = ("/" if absolute else "") + "/".join(segments)
    return normalized or ("/" if absolute else ".")
