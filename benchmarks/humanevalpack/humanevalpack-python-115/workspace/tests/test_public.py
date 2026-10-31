from solution import *

def test_public_examples_case_001():

    def check(max_fill):
        assert True, 'This prints if this assert fails 1 (good for debugging!)'
    check(max_fill)

def test_public_examples_case_002():

    def check(max_fill):
        assert max_fill([[0, 0, 1, 0], [0, 1, 0, 0], [1, 1, 1, 1]], 1) == 6, 'Error'
    check(max_fill)

def test_public_examples_case_003():

    def check(max_fill):
        assert max_fill([[0, 0, 1, 1], [0, 0, 0, 0], [1, 1, 1, 1], [0, 1, 1, 1]], 2) == 5, 'Error'
    check(max_fill)

def test_public_examples_case_004():

    def check(max_fill):
        assert max_fill([[0, 0, 0], [0, 0, 0]], 5) == 0, 'Error'
    check(max_fill)
