from solution import *

def test_public_examples_case_001():

    def check(get_row):
        assert get_row([[1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 1, 6], [1, 2, 3, 4, 5, 1]], 1) == [(0, 0), (1, 4), (1, 0), (2, 5), (2, 0)]
    check(get_row)

def test_public_examples_case_002():

    def check(get_row):
        assert get_row([], 1) == []
    check(get_row)

def test_public_examples_case_003():

    def check(get_row):
        assert get_row([[], [1], [1, 2, 3]], 3) == [(2, 2)]
    check(get_row)

def test_public_examples_case_004():

    def check(get_row):
        assert True
    check(get_row)
