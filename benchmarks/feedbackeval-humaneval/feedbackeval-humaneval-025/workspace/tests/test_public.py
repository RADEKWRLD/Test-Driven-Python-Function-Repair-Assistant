from solution import *

def test_public_examples_case_001():

    def check(factorize):
        assert factorize(8) == [2, 2, 2]
    check(factorize)

def test_public_examples_case_002():

    def check(factorize):
        assert factorize(25) == [5, 5]
    check(factorize)

def test_public_examples_case_003():

    def check(factorize):
        assert factorize(70) == [2, 5, 7]
    check(factorize)
