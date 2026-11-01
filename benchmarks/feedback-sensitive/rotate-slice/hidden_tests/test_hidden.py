from solution import rotate_slice


def test_empty_input_with_clamped_negative_bounds():
    assert rotate_slice([], -99, 99, -4) == []


def test_out_of_range_bounds_select_the_whole_list():
    assert rotate_slice([2, 4, 6, 8], -20, 20, 5) == [8, 2, 4, 6]


def test_single_selected_element_is_unchanged():
    assert rotate_slice([1, 3, 5, 7], 1, 2, 100) == [1, 3, 5, 7]


def test_reversed_negative_bounds_select_nothing():
    assert rotate_slice([1, 3, 5], -1, -3, 5) == [1, 3, 5]


def test_start_beyond_end_selects_nothing():
    assert rotate_slice([5, 6, 7], 9, 20, -2) == [5, 6, 7]


def test_multiple_of_selected_length_is_unchanged():
    assert rotate_slice([0, 2, 4, 6, 8, 10], 1, 4, 3) == [0, 2, 4, 6, 8, 10]


def test_large_positive_steps_wrap_within_subslice():
    assert rotate_slice([1, 2, 3, 4, 5, 6, 7], 2, 6, 10) == [1, 2, 5, 6, 3, 4, 7]


def test_negative_steps_with_clamped_start():
    assert rotate_slice([3, 6, 9, 12, 15], -99, -1, -2) == [9, 12, 3, 6, 15]


def test_duplicates_and_input_identity_are_preserved():
    items = [6, 6, 1, 2, 1, 9]
    before = items.copy()
    actual = rotate_slice(items, 1, 5, 7)
    assert items == before
    assert actual is not items
    assert actual == [6, 1, 2, 1, 6, 9]


def test_bounded_slices_match_repeated_single_step_rotation():
    items = [0, 1, 2, 3]
    for start in range(-7, 8):
        for stop in range(-7, 8):
            for steps in range(-7, 8):
                expected = items.copy()
                selected = expected[start:stop]
                if selected:
                    for _ in range(abs(steps)):
                        if steps > 0:
                            selected = selected[-1:] + selected[:-1]
                        else:
                            selected = selected[1:] + selected[:1]
                expected[start:stop] = selected
                assert rotate_slice(items, start, stop, steps) == expected, (start, stop, steps)
