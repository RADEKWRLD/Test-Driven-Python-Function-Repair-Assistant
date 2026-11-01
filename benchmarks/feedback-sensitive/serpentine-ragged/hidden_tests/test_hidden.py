from solution import serpentine_ragged


def test_all_rows_empty():
    assert serpentine_ragged([[], []]) == []


def test_singleton_rows_preserve_all_values():
    assert serpentine_ragged([[9], [], [-4], [0]]) == [9, -4, 0]


def test_three_empty_rows_between_nonempty_rows():
    assert serpentine_ragged([[8, 9], [], [], [], [10, 11, 12]]) == [8, 9, 12, 11, 10]


def test_trailing_empty_rows():
    assert serpentine_ragged([[-1, 0, 1], [2, 3], [], []]) == [-1, 0, 1, 3, 2]


def test_multiple_leading_empty_rows():
    assert serpentine_ragged([[], [], [], [6, 7], [8, 9]]) == [6, 7, 9, 8]


def test_unequal_lengths_without_empty_rows():
    rows = [[1, 4, 7], [2], [3, 6], [-1, -2, -3, -4]]
    assert serpentine_ragged(rows) == [1, 4, 7, 2, 3, 6, -4, -3, -2, -1]


def test_negative_duplicates_survive_reversal():
    rows = [[-2, -2, 0], [], [0, -2, -2], [-5]]
    assert serpentine_ragged(rows) == [-2, -2, 0, -2, -2, 0, -5]


def test_direction_counts_only_nonempty_rows_over_many_turns():
    rows = [[1, 2], [], [3, 4], [], [5, 6], [], [7, 8]]
    assert serpentine_ragged(rows) == [1, 2, 4, 3, 5, 6, 8, 7]


def test_inner_and_outer_lists_remain_unchanged():
    rows = [[7, 6], [], [5, 4, 3], [2]]
    before = [row.copy() for row in rows]
    row_ids = [id(row) for row in rows]
    actual = serpentine_ragged(rows)
    assert rows == before
    assert [id(row) for row in rows] == row_ids
    assert actual == [7, 6, 3, 4, 5, 2]
