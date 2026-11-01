import pytest

from solution import subtract_interval


def test_external_cuts_clip_at_both_source_ends():
    assert subtract_interval((-2, 7), [(-9, 0), (5, 12)]) == [(0, 5)]


def test_cuts_touching_only_outer_endpoints_remove_nothing():
    assert subtract_interval((3, 8), [(0, 3), (8, 10)]) == [(3, 8)]


def test_zero_length_cuts_remove_no_points():
    assert subtract_interval((-4, 4), [(-4, -4), (0, 0), (4, 4)]) == [(-4, 4)]


def test_duplicate_cuts_do_not_change_union():
    assert subtract_interval((0, 12), [(2, 9), (2, 9)]) == [(0, 2), (9, 12)]


def test_negative_source_with_disjoint_cuts():
    cuts = [(-9, -7), (-5, -3)]
    assert subtract_interval((-10, -1), cuts) == [(-10, -9), (-7, -5), (-3, -1)]
    assert cuts == [(-9, -7), (-5, -3)]


def test_nested_cut_cannot_open_gap_before_later_overlap():
    assert subtract_interval((0, 15), [(2, 10), (3, 4), (8, 12)]) == [(0, 2), (12, 15)]


def test_covering_cut_followed_by_nested_cut_still_removes_all():
    assert subtract_interval((1, 9), [(0, 12), (3, 5)]) == []


def test_reversed_source_is_rejected():
    with pytest.raises(ValueError):
        subtract_interval((7, 6), [])


def test_invalid_cut_is_rejected_even_for_empty_source():
    with pytest.raises(ValueError):
        subtract_interval((0, 0), [(-2, 2), (9, 8)])


def test_bounded_cut_pairs_match_independent_point_membership():
    choices = [(-5, -1), (-2, 2), (-1, 0), (0, 0), (1, 5), (-5, 5)]
    for first in choices:
        for second in choices:
            survivors = [
                point for point in range(-3, 4)
                if not any(left <= point < right for left, right in (first, second))
            ]
            expected = []
            for point in survivors:
                if expected and expected[-1][1] == point:
                    expected[-1] = (expected[-1][0], point + 1)
                else:
                    expected.append((point, point + 1))
            assert subtract_interval((-3, 4), [second, first]) == expected, (first, second)
