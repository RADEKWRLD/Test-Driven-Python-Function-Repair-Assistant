from solution import *

def test_hidden_suite_case_001():

    def check(count_nums):
        assert count_nums([]) == 0
    check(count_nums)

def test_hidden_suite_case_002():

    def check(count_nums):
        assert count_nums([-1, -2, 0]) == 0
    check(count_nums)

def test_hidden_suite_case_003():

    def check(count_nums):
        assert count_nums([1, 1, 2, -2, 3, 4, 5]) == 6
    check(count_nums)

def test_hidden_suite_case_004():

    def check(count_nums):
        assert count_nums([1, 6, 9, -6, 0, 1, 5]) == 5
    check(count_nums)

def test_hidden_suite_case_005():

    def check(count_nums):
        assert count_nums([1, 100, 98, -7, 1, -1]) == 4
    check(count_nums)

def test_hidden_suite_case_006():

    def check(count_nums):
        assert count_nums([12, 23, 34, -45, -56, 0]) == 5
    check(count_nums)

def test_hidden_suite_case_007():

    def check(count_nums):
        assert count_nums([-0, 1 ** 0]) == 1
    check(count_nums)

def test_hidden_suite_case_008():

    def check(count_nums):
        assert count_nums([1]) == 1
    check(count_nums)

def test_hidden_suite_case_009():

    def check(count_nums):
        assert True, 'This prints if this assert fails 2 (also good for debugging!)'
    check(count_nums)
