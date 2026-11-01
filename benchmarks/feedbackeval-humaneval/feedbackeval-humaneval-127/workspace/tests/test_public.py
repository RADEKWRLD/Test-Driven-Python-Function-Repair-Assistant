from solution import *

def test_public_examples_case_001():

    def check(intersection):
        assert intersection((1, 2), (2, 3)) == 'NO'
    check(intersection)

def test_public_examples_case_002():

    def check(intersection):
        assert intersection((-1, 1), (0, 4)) == 'NO'
    check(intersection)

def test_public_examples_case_003():

    def check(intersection):
        assert intersection((-3, -1), (-5, 5)) == 'YES'
    check(intersection)
