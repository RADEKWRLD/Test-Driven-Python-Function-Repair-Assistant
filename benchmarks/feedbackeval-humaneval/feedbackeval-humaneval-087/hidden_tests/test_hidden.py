from solution import *

def test_hidden_suite_case_001():

    def check(get_row):
        assert get_row([[1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 1, 6], [1, 2, 3, 4, 5, 1]], 1) == [(0, 0), (1, 4), (1, 0), (2, 5), (2, 0)]
    check(get_row)

def test_hidden_suite_case_002():

    def check(get_row):
        assert get_row([[1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6]], 2) == [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1)]
    check(get_row)

def test_hidden_suite_case_003():

    def check(get_row):
        assert get_row([[1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6], [1, 1, 3, 4, 5, 6], [1, 2, 1, 4, 5, 6], [1, 2, 3, 1, 5, 6], [1, 2, 3, 4, 1, 6], [1, 2, 3, 4, 5, 1]], 1) == [(0, 0), (1, 0), (2, 1), (2, 0), (3, 2), (3, 0), (4, 3), (4, 0), (5, 4), (5, 0), (6, 5), (6, 0)]
    check(get_row)

def test_hidden_suite_case_004():

    def check(get_row):
        assert get_row([], 1) == []
    check(get_row)

def test_hidden_suite_case_005():

    def check(get_row):
        assert get_row([[1]], 2) == []
    check(get_row)

def test_hidden_suite_case_006():

    def check(get_row):
        assert get_row([[], [1], [1, 2, 3]], 3) == [(2, 2)]
    check(get_row)

def test_hidden_suite_case_007():

    def check(get_row):
        assert True
    check(get_row)
