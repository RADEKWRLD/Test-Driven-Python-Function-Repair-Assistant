import pytest

from solution import cap_runs


def test_single_none_is_not_confused_with_initial_state():
    assert cap_runs([None], 1) == [None]


def test_none_runs_reset_after_intervening_value():
    assert cap_runs([None, None, 4, None, None, None], 2) == [None, None, 4, None, None]


def test_alternating_values_are_all_separate_runs():
    assert cap_runs(["x", "y", "x", "y", "x", "y"], 1) == ["x", "y", "x", "y", "x", "y"]


def test_unhashable_values_and_input_are_preserved():
    items = [[1], [1], [2], [1]]
    result = cap_runs(items, 1)
    assert result == [[1], [2], [1]]
    assert items == [[1], [1], [2], [1]]
    assert result is not items


def test_zero_and_false_share_run_but_reset_after_separator():
    result = cap_runs([0, False, 0, "sep", False, 0], 1)
    assert result == [0, "sep", False]
    assert type(result[0]) is int
    assert result[2] is False


def test_large_limit_preserves_every_occurrence():
    items = [3, 3, -2, 3, 3, 3]
    result = cap_runs(items, 100)
    assert result == items
    assert result is not items


def test_empty_input_still_validates_negative_limit():
    with pytest.raises(ValueError):
        cap_runs([], -7)


def test_zero_limit_with_multiple_revisited_values():
    assert cap_runs(["r", "s", "r", "s"], 0) == []


def test_run_lengths_on_both_sides_of_cap():
    items = [9] * 2 + [8] * 3 + [9] * 4 + [8]
    assert cap_runs(items, 3) == [9] * 2 + [8] * 3 + [9] * 3 + [8]


def test_repeated_equal_but_differently_typed_values():
    result = cap_runs([1, True, 1.0, 2, True, 1, 1.0], 2)
    assert result == [1, True, 2, True, 1]
    assert [type(value) for value in result] == [int, bool, int, bool, int]
