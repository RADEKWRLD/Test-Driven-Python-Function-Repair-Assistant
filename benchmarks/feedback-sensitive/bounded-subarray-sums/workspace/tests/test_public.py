import pytest

from solution import count_bounded_sums


def test_empty_input():
    assert count_bounded_sums([], 0, 3) == 0


def test_length_equal_to_limit_counts():
    assert count_bounded_sums([1, 2, 3], 3, 2) == 2


def test_single_element_at_unit_limit():
    assert count_bounded_sums([4], 4, 1) == 1


def test_duplicate_zero_intervals_are_distinct():
    assert count_bounded_sums([0, 0], 0, 2) == 3


def test_negative_values_allow_cancellation():
    assert count_bounded_sums([2, -1, 2], 1, 3) == 2


def test_oversized_limit_permits_all_intervals():
    assert count_bounded_sums([1, 1, 1], 2, 10) == 2


def test_zero_limit_is_invalid_even_for_empty_input():
    with pytest.raises(ValueError):
        count_bounded_sums([], 0, 0)


def test_input_is_not_mutated():
    items = [3, -3, 2]
    before = items.copy()
    actual = count_bounded_sums(items, 2, 3)
    assert items == before
    assert actual == 2
