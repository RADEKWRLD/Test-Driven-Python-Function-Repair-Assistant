from itertools import product

from solution import multiset_intersection


def test_both_inputs_empty():
    assert multiset_intersection([], []) == []


def test_disjoint_inputs():
    assert multiset_intersection([1, 1, 3], [2, 2, 4]) == []


def test_unique_left_and_repeated_right():
    assert multiset_intersection([7, 8], [8, 8, 7, 7]) == [7, 8]


def test_one_right_occurrence_is_consumed_once():
    assert multiset_intersection([9, 9, 9], [9]) == [9]


def test_repeated_zero_values():
    assert multiset_intersection([0, 0, 1, 0], [0, 0, 0]) == [0, 0, 0]


def test_negative_duplicate_values():
    assert multiset_intersection([-3, -1, -3, -2, -1], [-1, -3, -3]) == [-3, -1, -3]


def test_duplicate_counts_do_not_change_left_order():
    assert multiset_intersection([5, 4, 3, 4, 5], [4, 5, 5, 4]) == [5, 4, 4, 5]


def test_identical_inputs_preserve_all_occurrences():
    assert multiset_intersection([2, 1, 2, 3], [2, 1, 2, 3]) == [2, 1, 2, 3]


def test_inputs_remain_unchanged_after_multiple_consumptions():
    left = [8, 7, 8, 6]
    right = [8, 6, 8]
    left_before = left.copy()
    right_before = right.copy()
    actual = multiset_intersection(left, right)
    assert left == left_before
    assert right == right_before
    assert actual == [8, 8, 6]


def test_bounded_lists_match_independent_occurrence_removal():
    for left_values in product((-1, 0, 1), repeat=3):
        for right_values in product((-1, 0, 1), repeat=3):
            left = list(left_values)
            right = list(right_values)
            unused = right.copy()
            expected = []
            for value in left:
                if value in unused:
                    expected.append(value)
                    unused.remove(value)
            assert multiset_intersection(left, right) == expected, (left, right)
