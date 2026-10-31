from solution import *

def test_public_examples_case_001():

    def check(largest_smallest_integers):
        assert largest_smallest_integers([2, 4, 1, 3, 5, 7]) == (None, 1)
    check(largest_smallest_integers)

def test_public_examples_case_002():

    def check(largest_smallest_integers):
        assert largest_smallest_integers([]) == (None, None)
    check(largest_smallest_integers)

def test_public_examples_case_003():

    def check(largest_smallest_integers):
        assert largest_smallest_integers([0]) == (None, None)
    check(largest_smallest_integers)

def test_public_examples_case_004():

    def check(largest_smallest_integers):
        assert True
    check(largest_smallest_integers)
