import pytest

from solution import sliding_modes


def test_empty_input():
    assert sliding_modes([], 3) == []


def test_width_one_tracks_each_new_value():
    assert sliding_modes([2, 1, 3], 1) == [2, 1, 3]


def test_single_full_window_breaks_ties_by_smallest():
    assert sliding_modes([3, 2, 3, 2], 4) == [2]


def test_modes_change_as_repeated_values_leave():
    assert sliding_modes([1, 1, 2, 2, 3, 3], 2) == [1, 1, 2, 2, 3]


def test_evicted_small_value_no_longer_participates():
    assert sliding_modes([0, 3, 4], 2) == [0, 3]


def test_all_equal_values():
    assert sliding_modes([7, 7, 7], 2) == [7, 7]


def test_zero_width_is_invalid_even_for_empty_input():
    with pytest.raises(ValueError):
        sliding_modes([], 0)


def test_input_is_not_mutated():
    items = [5, 2, 5, 8]
    before = items.copy()
    actual = sliding_modes(items, 3)
    assert items == before
    assert actual == [5, 2]
