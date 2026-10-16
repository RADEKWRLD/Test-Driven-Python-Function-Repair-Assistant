import pytest

from solution import chunk_list


def test_empty_input():
    assert chunk_list([], 3) == []


def test_even_chunks():
    assert chunk_list([1, 2, 3, 4], 2) == [[1, 2], [3, 4]]


def test_partial_final_chunk():
    assert chunk_list([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]


def test_zero_size_rejected():
    with pytest.raises(ValueError):
        chunk_list([1], 0)


def test_input_not_mutated():
    values = [1, 2, 3]
    chunk_list(values, 2)
    assert values == [1, 2, 3]
