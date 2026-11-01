import pytest

from solution import map_after_deletions


def test_all_positions_deleted_with_unique_indices():
    assert map_after_deletions(3, [2, 0, 1]) == [None, None, None]


def test_duplicate_last_deletion_does_not_affect_earlier_survivors():
    assert map_after_deletions(4, [-1, 3, -1]) == [0, 1, 2, None]


def test_first_position_deleted_repeatedly():
    assert map_after_deletions(6, [0, 0, 0]) == [None, 0, 1, 2, 3, 4]


def test_unsorted_duplicates_and_negative_aliases():
    assert map_after_deletions(7, [4, -5, 2, -3, 4]) == [0, 1, None, 2, None, 3, 4]


def test_lowest_valid_negative_index_is_first_position():
    assert map_after_deletions(8, [-8, -2]) == [None, 0, 1, 2, 3, 4, None, 5]


def test_invalid_index_is_checked_after_valid_duplicate_indices():
    for invalid in (4, 9, -5, -9):
        with pytest.raises(ValueError):
            map_after_deletions(4, [1, 1, invalid])


def test_empty_original_rejects_every_deletion():
    for index in (0, -1, 1):
        with pytest.raises(ValueError):
            map_after_deletions(0, [index])


def test_negative_length_rejected_with_nonempty_removed_list():
    with pytest.raises(ValueError):
        map_after_deletions(-4, [0])


def test_input_order_and_duplicates_are_preserved():
    removed = [-6, 3, 0, -3]
    assert map_after_deletions(6, removed) == [None, 0, 1, None, 2, 3]
    assert removed == [-6, 3, 0, -3]


def test_bounded_deletions_match_survivor_enumeration():
    for length in range(1, 8):
        for first in range(-length, length):
            for second in range(-length, length):
                removed = [first, second, first]
                erased = {index % length for index in removed}
                survivors = [index for index in range(length) if index not in erased]
                lookup = {original: new for new, original in enumerate(survivors)}
                expected = [lookup.get(index) for index in range(length)]
                assert map_after_deletions(length, removed) == expected, (length, removed)
