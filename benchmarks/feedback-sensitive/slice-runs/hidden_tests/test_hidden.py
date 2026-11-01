import pytest

from solution import slice_runs


def test_only_zero_count_runs():
    assert slice_runs([(1, 0), (2, 0)], -9, 12) == []


def test_very_negative_start_clips_to_expanded_beginning():
    assert slice_runs([(-3, 2), (6, 4)], -100, 5) == [-3, -3, 6, 6, 6]


def test_positive_indices_beyond_expansion_return_empty():
    assert slice_runs([(8, 2), (1, 1)], 20, 30) == []


def test_overlarge_stop_clips_to_expanded_end():
    assert slice_runs([(2, 2), (7, 3)], 3, 100) == [7, 7]


def test_small_tail_of_large_run_does_not_need_full_expansion():
    assert slice_runs([(5, 10 ** 9)], 10 ** 9 - 3, 10 ** 9) == [5, 5, 5]


def test_empty_slice_of_large_run_remains_empty():
    assert slice_runs([(3, 10 ** 9), (1, 2)], 5, 5) == []


def test_negative_slice_spans_zero_and_repeated_runs():
    runs = [(4, 2), (99, 0), (-1, 3), (8, 1)]
    assert slice_runs(runs, -5, -1) == [4, -1, -1, -1]
    assert runs == [(4, 2), (99, 0), (-1, 3), (8, 1)]


def test_unit_runs_preserve_duplicate_values_and_new_result():
    runs = [(2, 1), (2, 1), (-4, 1), (2, 1)]
    result = slice_runs(runs, -3, 4)
    assert result == [2, -4, 2]
    assert result is not runs


def test_invalid_late_run_is_validated_outside_slice():
    with pytest.raises(ValueError):
        slice_runs([(6, 5), (9, -2)], 0, 1)


def test_bounded_runs_match_explicit_python_slice():
    for first_count in range(4):
        for second_count in range(4):
            runs = [(4, first_count), (-1, second_count)]
            expanded = [4] * first_count + [-1] * second_count
            for start in range(-6, 7):
                for stop in range(-6, 7):
                    assert slice_runs(runs, start, stop) == expanded[start:stop], (
                        runs, start, stop
                    )
