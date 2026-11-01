from solution import *

def test_public_examples_case_001():

    def check(triples_sum_to_zero):
        assert triples_sum_to_zero([1, 3, 5, 0]) == False
    check(triples_sum_to_zero)

def test_public_examples_case_002():

    def check(triples_sum_to_zero):
        assert triples_sum_to_zero([1, 3, -2, 1]) == True
    check(triples_sum_to_zero)

def test_public_examples_case_003():

    def check(triples_sum_to_zero):
        assert triples_sum_to_zero([1, 2, 3, 7]) == False
    check(triples_sum_to_zero)

def test_public_examples_case_004():

    def check(triples_sum_to_zero):
        assert triples_sum_to_zero([2, 4, -5, 3, 9, 7]) == True
    check(triples_sum_to_zero)
