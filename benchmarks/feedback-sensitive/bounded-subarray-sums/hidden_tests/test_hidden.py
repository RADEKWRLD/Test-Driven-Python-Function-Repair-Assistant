from itertools import product

import pytest

from solution import count_bounded_sums


def test_empty_input_with_nonzero_target():
    assert count_bounded_sums([], 5, 7) == 0


def test_no_matching_sum():
    assert count_bounded_sums([2, -2, 4], 99, 2) == 0


def test_all_zero_intervals_up_to_length_three():
    assert count_bounded_sums([0, 0, 0, 0], 0, 3) == 9


def test_boundary_and_shorter_matches_both_count():
    assert count_bounded_sums([3, 1, -2, 4], 2, 3) == 2


def test_negative_target_with_exact_length_match():
    assert count_bounded_sums([-2, -1, 3, -2], -3, 2) == 1


def test_overlapping_cancellations_are_separate_intervals():
    assert count_bounded_sums([1, -1, 1, -1], 0, 2) == 3


def test_unit_limit_counts_only_matching_elements():
    assert count_bounded_sums([5, 0, 5, -5], 5, 1) == 2


def test_limit_larger_than_input_with_negative_values():
    assert count_bounded_sums([-1, 2, -1], 1, 8) == 2


def test_negative_limit_is_invalid():
    with pytest.raises(ValueError):
        count_bounded_sums([0], 0, -2)


def test_bounded_inputs_match_direct_interval_enumeration():
    for values in product((-1, 0, 1), repeat=4):
        items = list(values)
        for max_length in range(1, 6):
            for target in range(-2, 3):
                expected = sum(
                    sum(items[start:stop]) == target
                    for start in range(len(items))
                    for stop in range(start + 1, min(len(items), start + max_length) + 1)
                )
                before = items.copy()
                actual = count_bounded_sums(items, target, max_length)
                assert items == before
                assert actual == expected, (items, target, max_length)
