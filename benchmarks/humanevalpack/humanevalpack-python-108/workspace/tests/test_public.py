from solution import *

def test_public_examples_case_001():

    def check(count_nums):
        assert count_nums([]) == 0
    check(count_nums)

def test_public_examples_case_002():

    def check(count_nums):
        assert count_nums([-1, 11, -11]) == 1
    check(count_nums)

def test_public_examples_case_003():

    def check(count_nums):
        assert count_nums([1, 1, 2]) == 3
    check(count_nums)

def test_public_examples_case_004():

    def check(count_nums):
        assert True, 'This prints if this assert fails 2 (also good for debugging!)'
    check(count_nums)
