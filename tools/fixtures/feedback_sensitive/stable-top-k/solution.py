def stable_top_k(records, k):
    """Reference implementation; keep outside the model workspace."""
    if k < 0:
        raise ValueError("k must be nonnegative")

    indexed = list(enumerate(records))
    ranked = sorted(
        indexed,
        key=lambda entry: (-entry[1][1], entry[0]),
    )

    labels = []
    for _, record in ranked[:k]:
        label, _ = record
        labels.append(label)
    return labels
