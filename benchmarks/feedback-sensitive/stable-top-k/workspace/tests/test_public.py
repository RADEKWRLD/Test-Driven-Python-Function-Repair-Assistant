import pytest

from solution import stable_top_k


def test_empty_input():
    assert stable_top_k([], 0) == []


def test_zero_k_selects_nothing():
    assert stable_top_k([("a", 3), ("b", 4)], 0) == []


def test_distinct_scores_are_descending():
    assert stable_top_k([("low", 1), ("high", 3), ("mid", 2)], 2) == ["high", "mid"]


def test_equal_scores_keep_original_order():
    assert stable_top_k([("a", 5), ("b", 5), ("c", 3)], 2) == ["a", "b"]


def test_tie_crosses_selection_boundary():
    records = [("a", 4), ("b", 2), ("c", 2), ("d", 1)]
    assert stable_top_k(records, 2) == ["a", "b"]


def test_identical_records_are_not_deduplicated():
    records = [("same", 2), ("same", 2), ("low", 1)]
    assert stable_top_k(records, 3) == ["same", "same", "low"]


def test_negative_k_is_invalid_even_for_empty_input():
    with pytest.raises(ValueError):
        stable_top_k([], -1)


def test_input_is_not_mutated():
    records = [("z", 1), ("x", 1), ("y", 2)]
    before = records.copy()
    actual = stable_top_k(records, 3)
    assert records == before
    assert actual == ["y", "z", "x"]
