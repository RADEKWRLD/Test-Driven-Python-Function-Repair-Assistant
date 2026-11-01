from solution import rotate_slice


def test_empty_input():
    assert rotate_slice([], 0, 3, 2) == []


def test_whole_list_rotation():
    assert rotate_slice([1, 2, 3, 4], 0, 4, 1) == [4, 1, 2, 3]


def test_rotation_wraps_at_selected_length():
    assert rotate_slice([0, 1, 2, 3, 4], 1, 4, 4) == [0, 3, 1, 2, 4]


def test_negative_steps_rotate_selected_slice_left():
    assert rotate_slice([10, 20, 30, 40, 50], 1, 4, -1) == [10, 30, 40, 20, 50]


def test_negative_slice_bounds():
    assert rotate_slice([1, 2, 3, 4, 5], -4, -1, 1) == [1, 4, 2, 3, 5]


def test_stop_before_start_selects_nothing():
    assert rotate_slice([1, 2, 3], 2, 1, 9) == [1, 2, 3]


def test_zero_rotation_preserves_values():
    assert rotate_slice([7, 8, 9], 1, 3, 0) == [7, 8, 9]


def test_input_is_not_mutated():
    items = [1, 2, 3, 4, 5, 6]
    before = items.copy()
    actual = rotate_slice(items, 1, 5, 6)
    assert items == before
    assert actual is not items
    assert actual == [1, 4, 5, 2, 3, 6]
