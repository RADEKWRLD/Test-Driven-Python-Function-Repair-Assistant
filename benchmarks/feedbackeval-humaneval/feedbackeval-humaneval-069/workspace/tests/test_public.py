from solution import *

def test_public_examples_case_001():

    def check(search):
        assert search([4, 1, 2, 2, 3, 1]) == 2
    check(search)

def test_public_examples_case_002():

    def check(search):
        assert search([1, 2, 2, 3, 3, 3, 4, 4, 4]) == 3
    check(search)

def test_public_examples_case_003():

    def check(search):
        assert search([5, 5, 4, 4, 4]) == -1
    check(search)
