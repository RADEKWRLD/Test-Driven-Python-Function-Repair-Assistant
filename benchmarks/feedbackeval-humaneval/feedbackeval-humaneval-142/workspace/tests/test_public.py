from solution import *

def test_public_examples_case_001():

    def check(sum_squares):
        assert sum_squares([1, 2, 3]) == 6
    check(sum_squares)

def test_public_examples_case_002():

    def check(sum_squares):
        assert sum_squares([]) == 0
    check(sum_squares)

def test_public_examples_case_003():

    def check(sum_squares):
        assert sum_squares([-1, -5, 2, -1, -5]) == -126
    check(sum_squares)
