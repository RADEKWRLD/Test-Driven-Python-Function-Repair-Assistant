from solution import *

def test_public_examples_case_001():

    def check(will_it_fly):
        assert will_it_fly([3, 2, 3], 9) is True
    check(will_it_fly)

def test_public_examples_case_002():

    def check(will_it_fly):
        assert will_it_fly([1, 2], 5) is False
    check(will_it_fly)

def test_public_examples_case_003():

    def check(will_it_fly):
        assert will_it_fly([3], 5) is True
    check(will_it_fly)

def test_public_examples_case_004():

    def check(will_it_fly):
        assert will_it_fly([3, 2, 3], 1) is False
    check(will_it_fly)
