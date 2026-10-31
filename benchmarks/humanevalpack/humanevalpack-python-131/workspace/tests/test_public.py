from solution import *

def test_public_examples_case_001():

    def check(digits):
        assert digits(1) == 1
    check(digits)

def test_public_examples_case_002():

    def check(digits):
        assert digits(4) == 0
    check(digits)

def test_public_examples_case_003():

    def check(digits):
        assert digits(235) == 15
    check(digits)
