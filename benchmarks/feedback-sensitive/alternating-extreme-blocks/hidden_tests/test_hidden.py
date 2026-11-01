import pytest

from solution import alternating_extreme_blocks


def test_empty_input_with_large_block():
    assert alternating_extreme_blocks([], 9) == []


def test_single_negative_value_with_partial_block():
    assert alternating_extreme_blocks([-8], 7) == [-8]


def test_block_larger_than_input():
    assert alternating_extreme_blocks([9, -1, 4, 4], 10) == [-1, 4, 4, 9]


def test_exactly_one_block():
    assert alternating_extreme_blocks([12, 0, -3, 6], 4) == [-3, 0, 6, 12]


def test_even_blocks_with_partial_low_tail():
    assert alternating_extreme_blocks(list(range(10)), 4) == [0, 1, 2, 3, 9, 8, 7, 6, 4, 5]


def test_odd_blocks_with_partial_high_tail():
    assert alternating_extreme_blocks(list(range(8, -2, -1)), 3) == [-1, 0, 1, 8, 7, 6, 2, 3, 4, 5]


def test_negative_values_across_multiple_turns():
    values = [-1, -9, -2, -8, -3, -7, -4, -6, -5]
    assert alternating_extreme_blocks(values, 2) == [-9, -8, -1, -2, -7, -6, -3, -4, -5]


def test_equal_values_preserve_multiplicity():
    assert alternating_extreme_blocks([2] * 7, 2) == [2] * 7


def test_duplicate_values_cross_block_boundaries():
    values = [0, 2, 0, -2, 2, -2, 0, 2]
    assert alternating_extreme_blocks(values, 2) == [-2, -2, 2, 2, 0, 0, 2, 0]


def test_invalid_size_is_rejected_before_empty_shortcut():
    with pytest.raises(ValueError):
        alternating_extreme_blocks([], 0)


def test_negative_block_size():
    with pytest.raises(ValueError):
        alternating_extreme_blocks([8, 4], -3)


def test_unsorted_input_remains_unchanged():
    items = [7, 4, -1, 9, 2]
    before = items.copy()
    actual = alternating_extreme_blocks(items, 2)
    assert items == before
    assert actual == [-1, 2, 9, 7, 4]
