from solution import *

def test_public_examples_case_001():

    def check(by_length):
        assert True, 'This prints if this assert fails 1 (good for debugging!)'
    check(by_length)

def test_public_examples_case_002():

    def check(by_length):
        assert by_length([2, 1, 1, 4, 5, 8, 2, 3]) == ['Eight', 'Five', 'Four', 'Three', 'Two', 'Two', 'One', 'One'], 'Error'
    check(by_length)

def test_public_examples_case_003():

    def check(by_length):
        assert by_length([]) == [], 'Error'
    check(by_length)

def test_public_examples_case_004():

    def check(by_length):
        assert by_length([1, -1, 55]) == ['One'], 'Error'
    check(by_length)
