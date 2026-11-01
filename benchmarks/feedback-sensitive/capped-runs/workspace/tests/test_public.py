import pytest

from solution import cap_runs


def test_empty_input():
    assert cap_runs([], 2) == []


def test_single_long_run_is_capped():
    assert cap_runs([7, 7, 7, 7], 2) == [7, 7]


def test_different_runs_have_independent_allowances():
    assert cap_runs([1, 1, 2, 2, 3], 1) == [1, 2, 3]


def test_returning_value_begins_a_new_run():
    assert cap_runs([1, 1, 2, 1, 1], 1) == [1, 2, 1]


def test_limit_applies_to_each_run_not_total_occurrences():
    items = ["a", "a", "a", "b", "a", "a", "a"]
    assert cap_runs(items, 2) == ["a", "a", "b", "a", "a"]


def test_zero_limit_returns_empty_without_mutating_input():
    items = [None, None, "x"]
    assert cap_runs(items, 0) == []
    assert items == [None, None, "x"]


def test_negative_limit_is_rejected():
    with pytest.raises(ValueError):
        cap_runs([1], -1)


def test_python_equality_preserves_original_retained_types():
    result = cap_runs([False, 0, True, 1], 1)
    assert result == [False, True]
    assert result[0] is False
    assert result[1] is True
