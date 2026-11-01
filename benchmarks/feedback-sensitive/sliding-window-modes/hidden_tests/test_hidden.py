from itertools import product

import pytest

from solution import sliding_modes


def test_empty_input_with_another_width():
    assert sliding_modes([], 12) == []


def test_width_larger_than_input():
    assert sliding_modes([1, 3], 4) == []


def test_negative_values_and_frequency_ties():
    assert sliding_modes([-5, -2, -2, -5], 2) == [-5, -2, -5]


def test_smallest_negative_value_is_evicted():
    assert sliding_modes([-9, 4, 5, 6], 2) == [-9, 4, 5]


def test_modes_change_across_three_repeated_runs():
    assert sliding_modes([1, 1, 1, 2, 2, 2, 3, 3, 3], 3) == [1, 1, 2, 2, 2, 3, 3]


def test_unit_width_preserves_input_order():
    assert sliding_modes([8, 5, 9, -2, 6], 1) == [8, 5, 9, -2, 6]


def test_negative_width_is_invalid():
    with pytest.raises(ValueError):
        sliding_modes([4], -1)


def test_full_window_of_distinct_values():
    assert sliding_modes([-1, 0, 2, 3], 4) == [-1]


def test_bounded_windows_match_independent_recounting():
    for values in product((-1, 0, 1), repeat=4):
        items = list(values)
        for width in range(1, 6):
            expected = []
            for start in range(len(items) - width + 1):
                window = items[start:start + width]
                maximum = max(window.count(value) for value in window)
                expected.append(min(value for value in window if window.count(value) == maximum))
            assert sliding_modes(items, width) == expected, (items, width)


def test_repeated_values_do_not_mutate_input():
    items = [3, 0, 4, 4, 9]
    before = items.copy()
    actual = sliding_modes(items, 2)
    assert items == before
    assert actual == [0, 0, 4, 4]
