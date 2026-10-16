from solution import unique_stable


def test_empty_input():
    assert unique_stable([]) == []


def test_input_without_duplicates():
    assert unique_stable([1, 2, 3]) == [1, 2, 3]


def test_duplicate_keeps_first_position():
    assert unique_stable([3, 1, 3, 2]) == [3, 1, 2]


def test_all_values_equal():
    assert unique_stable(["x", "x", "x"]) == ["x"]


def test_input_is_not_mutated():
    values = [2, 1, 2]
    unique_stable(values)
    assert values == [2, 1, 2]
