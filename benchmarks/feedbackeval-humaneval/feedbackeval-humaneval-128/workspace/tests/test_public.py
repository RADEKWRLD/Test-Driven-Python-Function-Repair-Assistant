from solution import *

def test_public_examples_case_001():

    def check(prod_signs):
        assert True, 'This prints if this assert fails 1 (good for debugging!)'
    check(prod_signs)

def test_public_examples_case_002():

    def check(prod_signs):
        assert prod_signs([1, 2, 2, -4]) == -9
    check(prod_signs)

def test_public_examples_case_003():

    def check(prod_signs):
        assert prod_signs([0, 1]) == 0
    check(prod_signs)

def test_public_examples_case_004():

    def check(prod_signs):
        assert prod_signs([]) == None
    check(prod_signs)
