def bucket_intervals(intervals, width):
    """Sum coverage of integer half-open intervals in signed width-sized buckets.

    Bucket k is [k*width, (k+1)*width). Return sorted (k, total) tuples with
    positive totals. Count overlapping/duplicate intervals separately. Empty
    intervals contribute nothing. Integer arithmetic must be exact. Raise
    ValueError for width <= 0 or end < start, and never mutate inputs.
    """
    if width <= 0:
        raise ValueError("width must be positive")
    totals = {}
    for start, end in intervals:
        if end < start:
            raise ValueError("end must not precede start")
        if start == end:
            continue
        first = int(start / width)
        last = int((end - 1) / width)
        for bucket in range(first, last + 1):
            overlap = min(end, (bucket + 1) * width) - max(start, bucket * width)
            if overlap > 0:
                totals[bucket] = totals.get(bucket, 0) + overlap
    return sorted(totals.items())
