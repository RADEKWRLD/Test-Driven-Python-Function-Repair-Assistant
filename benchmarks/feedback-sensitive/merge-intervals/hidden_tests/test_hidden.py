import pytest

from solution import merge_intervals


def test_only_empty_intervals():
    assert merge_intervals([(-5, -5), (7, 7)]) == []


def test_duplicate_intervals_contribute_once():
    assert merge_intervals([(4, 9), (4, 9), (4, 9)]) == [(4, 9)]


def test_multiple_overlaps_form_one_chain():
    assert merge_intervals([(8, 12), (2, 6), (5, 9)]) == [(2, 12)]


def test_nested_interval_cannot_disconnect_later_overlap():
    assert merge_intervals([(-4, 8), (-2, 1), (4, 10)]) == [(-4, 10)]


def test_negative_nested_intervals():
    assert merge_intervals([(-12, -2), (-9, -4), (-8, -7)]) == [(-12, -2)]


def test_identical_starts_keep_farthest_endpoint():
    assert merge_intervals([(5, 11), (5, 7), (5, 9)]) == [(5, 11)]


def test_touching_chain_with_empty_interval():
    assert merge_intervals([(3, 4), (1, 2), (2, 3), (2, 2)]) == [(1, 4)]


def test_large_integer_endpoints_are_exact():
    origin = 10 ** 20
    intervals = [(origin, origin + 11), (origin + 2, origin + 3)]
    assert merge_intervals(intervals) == [(origin, origin + 11)]
    assert intervals == [(origin, origin + 11), (origin + 2, origin + 3)]


def test_validation_does_not_skip_invalid_pair_after_empty_pair():
    with pytest.raises(ValueError):
        merge_intervals([(1, 1), (-2, -3)])


def test_bounded_pairs_match_independent_unit_coverage():
    examples = [(-3, -1), (-2, 2), (-1, 0), (0, 0), (1, 3), (-3, 3)]
    for first in examples:
        for second in examples:
            covered = sorted(set(range(*first)) | set(range(*second)))
            expected = []
            for point in covered:
                if expected and expected[-1][1] == point:
                    expected[-1] = (expected[-1][0], point + 1)
                else:
                    expected.append((point, point + 1))
            assert merge_intervals([second, first]) == expected, (first, second)
