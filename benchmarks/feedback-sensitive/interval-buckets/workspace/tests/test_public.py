import pytest

from solution import bucket_intervals


def test_empty_intervals():
    assert bucket_intervals([], 4) == []


def test_positive_interval_spans_partial_buckets():
    assert bucket_intervals([(1, 7)], 3) == [(0, 2), (1, 3), (2, 1)]


def test_end_boundary_is_excluded():
    assert bucket_intervals([(0, 6)], 3) == [(0, 3), (1, 3)]


def test_negative_partial_bucket_is_not_dropped():
    assert bucket_intervals([(-3, 1)], 2) == [(-2, 1), (-1, 2), (0, 1)]


def test_entirely_negative_interval():
    assert bucket_intervals([(-5, -1)], 3) == [(-2, 2), (-1, 2)]


def test_overlapping_intervals_accumulate():
    assert bucket_intervals([(0, 3), (1, 4)], 2) == [(0, 3), (1, 3)]


def test_zero_length_intervals_are_ignored():
    assert bucket_intervals([(2, 2), (5, 5)], 2) == []


def test_invalid_width_and_reversed_interval():
    with pytest.raises(ValueError):
        bucket_intervals([], 0)
    with pytest.raises(ValueError):
        bucket_intervals([(3, 2)], 2)
