from solution import *

def test_public_examples_case_001():

    def check(is_simple_power):
        assert is_simple_power(1, 4) == True, 'This prints if this assert fails 1 (good for debugging!)'
    check(is_simple_power)

def test_public_examples_case_002():

    def check(is_simple_power):
        assert is_simple_power(2, 2) == True, 'This prints if this assert fails 1 (good for debugging!)'
    check(is_simple_power)

def test_public_examples_case_003():

    def check(is_simple_power):
        assert is_simple_power(8, 2) == True, 'This prints if this assert fails 1 (good for debugging!)'
    check(is_simple_power)

def test_public_examples_case_004():

    def check(is_simple_power):
        assert is_simple_power(3, 2) == False, 'This prints if this assert fails 1 (good for debugging!)'
    check(is_simple_power)

def test_public_examples_case_005():

    def check(is_simple_power):
        assert is_simple_power(3, 1) == False, 'This prints if this assert fails 1 (good for debugging!)'
    check(is_simple_power)

def test_public_examples_case_006():

    def check(is_simple_power):
        assert is_simple_power(5, 3) == False, 'This prints if this assert fails 1 (good for debugging!)'
    check(is_simple_power)
