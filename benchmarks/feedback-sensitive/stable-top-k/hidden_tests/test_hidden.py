from itertools import product

import pytest

from solution import stable_top_k


def test_empty_input_with_positive_k():
    assert stable_top_k([], 8) == []


def test_negative_scores_with_ties():
    records = [("a", -1), ("b", -3), ("c", -1), ("d", 0)]
    assert stable_top_k(records, 4) == ["d", "a", "c", "b"]


def test_all_tied_scores_preserve_prefix():
    records = [("p", 7), ("q", 7), ("r", 7), ("s", 7)]
    assert stable_top_k(records, 3) == ["p", "q", "r"]


def test_oversized_k_returns_every_record():
    records = [("four", 4), ("two", 2), ("three", 3)]
    assert stable_top_k(records, 99) == ["four", "three", "two"]


def test_unit_k_chooses_earliest_tied_record():
    assert stable_top_k([("early", 9), ("later", 9), ("zero", 0)], 1) == ["early"]


def test_duplicate_labels_can_have_different_scores():
    records = [("x", 4), ("y", 3), ("x", 2), ("z", 3)]
    assert stable_top_k(records, 4) == ["x", "y", "z", "x"]


def test_identical_records_preserve_multiplicity_at_cutoff():
    assert stable_top_k([("a", 1), ("a", 1), ("b", 1)], 2) == ["a", "a"]


def test_negative_k_with_nonempty_input():
    with pytest.raises(ValueError):
        stable_top_k([("a", 1)], -5)


def test_input_with_separated_ties_remains_unchanged():
    records = [("m", 0), ("n", 4), ("o", 0), ("p", 2)]
    before = records.copy()
    actual = stable_top_k(records, 3)
    assert records == before
    assert actual == ["n", "p", "m"]


def test_bounded_scores_match_independent_pairwise_ranks():
    for scores in product((-1, 0, 1), repeat=4):
        records = [(f"row{index}", score) for index, score in enumerate(scores)]
        by_rank = [None] * len(records)
        for index, (label, score) in enumerate(records):
            rank = sum(
                other_score > score or (other_score == score and other_index < index)
                for other_index, (_, other_score) in enumerate(records)
            )
            by_rank[rank] = label
        for k in range(6):
            assert stable_top_k(records, k) == by_rank[:k], (records, k)
