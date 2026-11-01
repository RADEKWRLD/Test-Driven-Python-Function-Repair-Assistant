from solution import serpentine_ragged


def test_empty_outer_list():
    assert serpentine_ragged([]) == []


def test_adjacent_rows_alternate():
    assert serpentine_ragged([[1, 2], [3, 4]]) == [1, 2, 4, 3]


def test_empty_row_does_not_advance_direction():
    assert serpentine_ragged([[1, 2], [], [3, 4]]) == [1, 2, 4, 3]


def test_leading_empty_row_does_not_reverse_first_row():
    assert serpentine_ragged([[], [1, 2]]) == [1, 2]


def test_duplicates_are_not_deduplicated():
    assert serpentine_ragged([[2, 2], [], [3, 3, 1]]) == [2, 2, 1, 3, 3]


def test_consecutive_empty_rows_and_singletons():
    assert serpentine_ragged([[1], [], [], [2, 3], [4]]) == [1, 3, 2, 4]


def test_nested_input_is_not_mutated():
    rows = [[5, 1], [3, 2]]
    before = [row.copy() for row in rows]
    actual = serpentine_ragged(rows)
    assert rows == before
    assert actual == [5, 1, 2, 3]
