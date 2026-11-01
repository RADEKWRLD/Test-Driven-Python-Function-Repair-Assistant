from solution import multiset_intersection


def test_empty_left():
    assert multiset_intersection([], [1, 1]) == []


def test_empty_right():
    assert multiset_intersection([1, 2], []) == []


def test_distinct_values_preserve_left_order():
    assert multiset_intersection([3, 1, 2], [2, 3]) == [3, 2]


def test_left_duplicates_are_limited_by_right_count():
    assert multiset_intersection([2, 2, 2], [2, 2]) == [2, 2]


def test_extra_right_duplicates_do_not_create_new_values():
    assert multiset_intersection([1, 1, 2], [1, 1, 1, 2]) == [1, 1, 2]


def test_interleaved_duplicate_values_keep_left_order():
    assert multiset_intersection([1, 2, 1, 2, 1], [2, 1, 2, 1]) == [1, 2, 1, 2]


def test_negative_values():
    assert multiset_intersection([-1, 0, -2], [-2, -1]) == [-1, -2]


def test_both_inputs_are_not_mutated():
    left = [4, 4, 5]
    right = [4, 4, 6]
    left_before = left.copy()
    right_before = right.copy()
    actual = multiset_intersection(left, right)
    assert left == left_before
    assert right == right_before
    assert actual == [4, 4]
