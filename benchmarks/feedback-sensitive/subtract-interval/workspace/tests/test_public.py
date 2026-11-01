import pytest

from solution import subtract_interval


def test_empty_source():
    assert subtract_interval((2, 2), []) == []


def test_no_cuts_preserves_source_range():
    assert subtract_interval((1, 6), []) == [(1, 6)]


def test_middle_cut_splits_source():
    assert subtract_interval((0, 10), [(3, 7)]) == [(0, 3), (7, 10)]


def test_covering_cut_removes_everything():
    assert subtract_interval((2, 5), [(0, 8)]) == []


def test_separate_cuts_leave_multiple_pieces():
    assert subtract_interval((0, 9), [(1, 3), (5, 7)]) == [(0, 1), (3, 5), (7, 9)]


def test_unsorted_overlaps_do_not_mutate_cuts():
    cuts = [(4, 8), (2, 5)]
    assert subtract_interval((0, 10), cuts) == [(0, 2), (8, 10)]
    assert cuts == [(4, 8), (2, 5)]


def test_nested_cut_does_not_move_cursor_backwards():
    assert subtract_interval((0, 10), [(2, 8), (3, 4)]) == [(0, 2), (8, 10)]


def test_reversed_cut_is_rejected():
    with pytest.raises(ValueError):
        subtract_interval((0, 5), [(4, 2)])
