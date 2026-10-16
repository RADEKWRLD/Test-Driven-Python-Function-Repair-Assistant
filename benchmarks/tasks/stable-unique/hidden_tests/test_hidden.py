from solution import unique_stable


def test_nonconsecutive_duplicates():
    assert unique_stable(["b", "a", "b", "c", "a"]) == ["b", "a", "c"]


def test_negative_boundary_values():
    assert unique_stable([0, -1, 0, -2, -1]) == [0, -1, -2]


def test_tuple_values_are_supported():
    assert unique_stable([(1, 2), (1, 2), (2, 1)]) == [(1, 2), (2, 1)]


def test_single_item():
    marker = ("only",)
    assert unique_stable([marker]) == [marker]


def test_late_repeat_does_not_move_first_item():
    assert unique_stable([9, 8, 7, 8, 9]) == [9, 8, 7]
