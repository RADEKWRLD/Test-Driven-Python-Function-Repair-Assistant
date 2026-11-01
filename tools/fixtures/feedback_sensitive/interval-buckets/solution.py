def bucket_intervals(intervals, width):
    if width <= 0:
        raise ValueError("width must be positive")
    totals = {}
    for start, end in intervals:
        if end < start:
            raise ValueError("end must not precede start")
        if start == end:
            continue
        first = start // width
        last = (end - 1) // width
        for bucket in range(first, last + 1):
            overlap = min(end, (bucket + 1) * width) - max(start, bucket * width)
            if overlap > 0:
                totals[bucket] = totals.get(bucket, 0) + overlap
    return sorted(totals.items())
