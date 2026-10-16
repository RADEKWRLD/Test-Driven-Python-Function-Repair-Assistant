import pytest

from solution import chunk_list


def test_single_item_is_one_chunk():
    assert chunk_list(["x"], 4) == [["x"]]


def test_size_larger_than_input():
    assert chunk_list([1, 2], 10) == [[1, 2]]


def test_size_one():
    assert chunk_list([1, 2, 3], 1) == [[1], [2], [3]]


def test_exact_boundary_has_no_empty_chunk():
    assert chunk_list([1, 2, 3, 4, 5, 6], 3) == [[1, 2, 3], [4, 5, 6]]


def test_negative_size_rejected():
    with pytest.raises(ValueError):
        chunk_list([1, 2], -1)
