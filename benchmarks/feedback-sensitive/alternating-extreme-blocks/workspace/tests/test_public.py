import pytest

from solution import alternating_extreme_blocks


def test_empty_input():
    assert alternating_extreme_blocks([], 3) == []


def test_singleton():
    assert alternating_extreme_blocks([5], 1) == [5]


def test_unit_blocks_alternate_extremes():
    assert alternating_extreme_blocks([4, 1, 3, 2], 1) == [1, 4, 2, 3]


def test_even_blocks_alternate_as_whole_blocks():
    assert alternating_extreme_blocks([6, 1, 5, 2, 4, 3], 2) == [1, 2, 6, 5, 3, 4]


def test_duplicate_occurrences_are_preserved():
    assert alternating_extreme_blocks([3, 1, 3, 2, 1, 2], 2) == [1, 1, 3, 3, 2, 2]


def test_zero_block_size_is_invalid():
    with pytest.raises(ValueError):
        alternating_extreme_blocks([1], 0)


def test_input_is_not_mutated():
    items = [8, 2, 6, 4]
    before = items.copy()
    actual = alternating_extreme_blocks(items, 2)
    assert items == before
    assert actual == [2, 4, 8, 6]
