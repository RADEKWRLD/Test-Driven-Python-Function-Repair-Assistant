import pytest

from solution import merge_intervals


def test_empty_input():
    assert merge_intervals([]) == []


def test_single_interval():
    assert merge_intervals([(2, 5)]) == [(2, 5)]


def test_disjoint_input_is_sorted_without_mutation():
    intervals = [(6, 8), (0, 2), (3, 4)]
    assert merge_intervals(intervals) == [(0, 2), (3, 4), (6, 8)]
    assert intervals == [(6, 8), (0, 2), (3, 4)]


def test_touching_endpoints_merge():
    assert merge_intervals([(1, 3), (3, 5)]) == [(1, 5)]


def test_overlap_can_extend_right_endpoint():
    assert merge_intervals([(1, 4), (2, 7)]) == [(1, 7)]


def test_nested_interval_does_not_shrink_coverage():
    assert merge_intervals([(0, 10), (2, 3)]) == [(0, 10)]


def test_empty_intervals_do_not_create_coverage():
    assert merge_intervals([(0, 0), (1, 3), (2, 2), (6, 6)]) == [(1, 3)]


def test_reversed_interval_is_rejected():
    with pytest.raises(ValueError):
        merge_intervals([(3, 2)])
