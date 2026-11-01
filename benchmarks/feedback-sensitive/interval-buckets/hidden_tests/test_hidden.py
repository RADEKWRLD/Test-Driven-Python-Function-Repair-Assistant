import pytest

from solution import bucket_intervals


def test_negative_exact_boundaries():
    assert bucket_intervals([(-8, -4)], 4) == [(-2, 4)]


def test_single_unit_at_minus_one():
    assert bucket_intervals([(-1, 0)], 7) == [(-1, 1)]


def test_both_sides_of_origin_have_correct_partial_lengths():
    assert bucket_intervals([(-7, 8)], 5) == [(-2, 2), (-1, 5), (0, 5), (1, 3)]


def test_duplicates_count_separately():
    assert bucket_intervals([(-2, 2), (-2, 2)], 3) == [(-1, 4), (0, 4)]


def test_result_sorted_even_for_unsorted_input():
    items = [(6, 8), (-4, -2), (2, 4)]
    assert bucket_intervals(items, 2) == [(-2, 2), (1, 2), (3, 2)]
    assert items == [(6, 8), (-4, -2), (2, 4)]


def test_zero_length_negative_intervals_add_no_buckets():
    assert bucket_intervals([(-9, -9), (-1, -1), (0, 0)], 4) == []


def test_negative_width_rejected_even_for_empty_input():
    with pytest.raises(ValueError):
        bucket_intervals([], -2)


def test_reversed_interval_after_valid_interval_is_rejected():
    with pytest.raises(ValueError):
        bucket_intervals([(0, 1), (-1, -3)], 3)


def test_large_coordinates_require_exact_integer_indices():
    start = 10 ** 18 + 1
    assert bucket_intervals([(start, start + 2)], 2) == [(start // 2, 1), (start // 2 + 1, 1)]
    start = -(10 ** 18) - 1
    assert bucket_intervals([(start, start + 2)], 2) == [(start // 2, 1), (start // 2 + 1, 1)]


def test_bounded_signed_intervals_match_unit_coverage():
    for width in (1, 2, 4):
        for start in range(-6, 7):
            for length in (1, 2, 5):
                end = start + length
                totals = {}
                for point in range(start, end):
                    bucket = point // width
                    totals[bucket] = totals.get(bucket, 0) + 1
                assert bucket_intervals([(start, end), (start, end)], width) == [
                    (bucket, overlap * 2) for bucket, overlap in sorted(totals.items())
                ], (width, start, end)
