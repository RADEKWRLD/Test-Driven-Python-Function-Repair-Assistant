import pytest

from solution import map_after_deletions


def test_empty_original_with_no_deletions():
    assert map_after_deletions(0, []) == []


def test_no_deletions_preserves_indices():
    assert map_after_deletions(4, []) == [0, 1, 2, 3]


def test_one_middle_deletion():
    assert map_after_deletions(5, [2]) == [0, 1, None, 2, 3]


def test_multiple_unique_deletions():
    assert map_after_deletions(6, [4, 1]) == [0, None, 1, 2, None, 3]


def test_negative_index_addresses_original_sequence():
    assert map_after_deletions(5, [-2]) == [0, 1, 2, None, 3]


def test_duplicate_deletions_shift_survivors_only_once():
    removed = [1, 1]
    assert map_after_deletions(4, removed) == [0, None, 1, 2]
    assert removed == [1, 1]


def test_negative_and_positive_alias_delete_same_position_once():
    assert map_after_deletions(5, [1, -4]) == [0, None, 1, 2, 3]


def test_negative_length_and_out_of_bounds_indices_are_rejected():
    with pytest.raises(ValueError):
        map_after_deletions(-1, [])
    with pytest.raises(ValueError):
        map_after_deletions(3, [3])
    with pytest.raises(ValueError):
        map_after_deletions(3, [-4])
