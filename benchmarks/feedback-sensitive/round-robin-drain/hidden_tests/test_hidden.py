from solution import round_robin_drain


def test_all_empty_rows():
    assert round_robin_drain([[], [], []]) == []


def test_one_nonempty_row_between_empty_rows():
    assert round_robin_drain([[], [9, 8, 7], []]) == [9, 8, 7]


def test_five_singletons_keep_original_row_order():
    assert round_robin_drain([[-2], [0], [2], [4], [6]]) == [-2, 0, 2, 4, 6]


def test_equal_rows_keep_order_during_last_round():
    rows = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    assert round_robin_drain(rows) == [1, 4, 7, 2, 5, 8, 3, 6, 9]


def test_middle_row_exhausts_first():
    assert round_robin_drain([[10, 11, 12], [20], [30, 31]]) == [10, 20, 30, 11, 31, 12]


def test_last_row_exhausts_first():
    assert round_robin_drain([[10, 11], [20, 21, 22], [30]]) == [10, 20, 30, 11, 21, 22]


def test_empty_rows_and_duplicate_values():
    rows = [[1, 1], [], [2], [], [], [3, 3, 3]]
    assert round_robin_drain(rows) == [1, 2, 3, 1, 3, 3]


def test_long_first_row_survives_other_rows():
    assert round_robin_drain([[-3, -2, -1, 0, 1], [8], [9]]) == [-3, 8, 9, -2, -1, 0, 1]


def test_long_last_row_survives_other_rows():
    assert round_robin_drain([[4], [5], [6, 7, 8, 9]]) == [4, 5, 6, 7, 8, 9]


def test_nested_values_and_row_identity_are_preserved():
    rows = [[6, -1], [4], [], [2, 8, 3]]
    before = [row.copy() for row in rows]
    row_ids = [id(row) for row in rows]
    actual = round_robin_drain(rows)
    assert rows == before
    assert [id(row) for row in rows] == row_ids
    assert actual == [6, 4, 2, -1, 8, 3]
