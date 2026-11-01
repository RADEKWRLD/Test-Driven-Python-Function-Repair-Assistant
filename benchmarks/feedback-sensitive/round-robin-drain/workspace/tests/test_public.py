from solution import round_robin_drain


def test_empty_outer_list():
    assert round_robin_drain([]) == []


def test_one_row_keeps_its_order():
    assert round_robin_drain([[2, 4, 6]]) == [2, 4, 6]


def test_two_equal_length_rows():
    assert round_robin_drain([[1, 2], [3, 4]]) == [1, 3, 2, 4]


def test_exhausted_row_does_not_skip_next_row():
    assert round_robin_drain([[1], [2], [3]]) == [1, 2, 3]


def test_ragged_rows_continue_after_first_row_finishes():
    assert round_robin_drain([[1], [2, 3], [4, 5]]) == [1, 2, 4, 3, 5]


def test_duplicate_occurrences_preserve_round_order():
    assert round_robin_drain([[7], [7, 8], [8, 7]]) == [7, 7, 8, 8, 7]


def test_nested_input_and_empty_rows_are_preserved():
    rows = [[], [0, 1], [], [2]]
    before = [row.copy() for row in rows]
    actual = round_robin_drain(rows)
    assert rows == before
    assert actual == [0, 2, 1]
