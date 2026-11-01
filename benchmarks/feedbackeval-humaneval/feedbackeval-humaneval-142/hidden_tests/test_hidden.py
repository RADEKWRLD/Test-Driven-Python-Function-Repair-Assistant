from solution import *

def test_hidden_suite_case_001():

    def check(sum_squares):
        assert sum_squares([1, 2, 3]) == 6
    check(sum_squares)

def test_hidden_suite_case_002():

    def check(sum_squares):
        assert sum_squares([1, 4, 9]) == 14
    check(sum_squares)

def test_hidden_suite_case_003():

    def check(sum_squares):
        assert sum_squares([]) == 0
    check(sum_squares)

def test_hidden_suite_case_004():

    def check(sum_squares):
        assert sum_squares([1, 1, 1, 1, 1, 1, 1, 1, 1]) == 9
    check(sum_squares)

def test_hidden_suite_case_005():

    def check(sum_squares):
        assert sum_squares([-1, -1, -1, -1, -1, -1, -1, -1, -1]) == -3
    check(sum_squares)

def test_hidden_suite_case_006():

    def check(sum_squares):
        assert sum_squares([0]) == 0
    check(sum_squares)

def test_hidden_suite_case_007():

    def check(sum_squares):
        assert sum_squares([-1, -5, 2, -1, -5]) == -126
    check(sum_squares)

def test_hidden_suite_case_008():

    def check(sum_squares):
        assert sum_squares([-56, -99, 1, 0, -2]) == 3030
    check(sum_squares)

def test_hidden_suite_case_009():

    def check(sum_squares):
        assert sum_squares([-1, 0, 0, 0, 0, 0, 0, 0, -1]) == 0
    check(sum_squares)

def test_hidden_suite_case_010():

    def check(sum_squares):
        assert sum_squares([-16, -9, -2, 36, 36, 26, -20, 25, -40, 20, -4, 12, -26, 35, 37]) == -14196
    check(sum_squares)

def test_hidden_suite_case_011():

    def check(sum_squares):
        assert sum_squares([-1, -3, 17, -1, -15, 13, -1, 14, -14, -12, -5, 14, -14, 6, 13, 11, 16, 16, 4, 10]) == -1448
    check(sum_squares)
