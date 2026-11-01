import pytest

from solution import slice_runs


def test_empty_runs():
    assert slice_runs([], 0, 4) == []


def test_unit_counts_match_plain_list_positions():
    assert slice_runs([(2, 1), (4, 1), (6, 1)], 1, 3) == [4, 6]


def test_slice_inside_repeated_run_uses_expanded_positions():
    assert slice_runs([(7, 5)], 1, 4) == [7, 7, 7]


def test_slice_crosses_run_boundary_without_mutation():
    runs = [(3, 3), (8, 2)]
    assert slice_runs(runs, 2, 5) == [3, 8, 8]
    assert runs == [(3, 3), (8, 2)]


def test_negative_indices_count_from_expanded_end():
    assert slice_runs([(1, 3), (2, 3)], -4, -1) == [1, 2, 2]


def test_zero_count_runs_do_not_add_positions():
    assert slice_runs([(9, 0), (4, 3), (8, 0)], 0, 3) == [4, 4, 4]


def test_reversed_slice_is_empty():
    assert slice_runs([(5, 2), (7, 2)], 3, 1) == []


def test_negative_count_rejected_even_for_empty_slice():
    with pytest.raises(ValueError):
        slice_runs([(1, -1)], 0, 0)
