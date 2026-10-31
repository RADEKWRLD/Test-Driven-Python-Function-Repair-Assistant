from solution import *

def test_hidden_suite_case_001():

    def check(minSubArraySum):
        assert minSubArraySum([2, 3, 4, 1, 2, 4]) == 1, 'This prints if this assert fails 1 (good for debugging!)'
    check(minSubArraySum)

def test_hidden_suite_case_002():

    def check(minSubArraySum):
        assert minSubArraySum([-1, -2, -3]) == -6
    check(minSubArraySum)

def test_hidden_suite_case_003():

    def check(minSubArraySum):
        assert minSubArraySum([-1, -2, -3, 2, -10]) == -14
    check(minSubArraySum)

def test_hidden_suite_case_004():

    def check(minSubArraySum):
        assert minSubArraySum([-9999999999999999]) == -9999999999999999
    check(minSubArraySum)

def test_hidden_suite_case_005():

    def check(minSubArraySum):
        assert minSubArraySum([0, 10, 20, 1000000]) == 0
    check(minSubArraySum)

def test_hidden_suite_case_006():

    def check(minSubArraySum):
        assert minSubArraySum([-1, -2, -3, 10, -5]) == -6
    check(minSubArraySum)

def test_hidden_suite_case_007():

    def check(minSubArraySum):
        assert minSubArraySum([100, -1, -2, -3, 10, -5]) == -6
    check(minSubArraySum)

def test_hidden_suite_case_008():

    def check(minSubArraySum):
        assert minSubArraySum([10, 11, 13, 8, 3, 4]) == 3
    check(minSubArraySum)

def test_hidden_suite_case_009():

    def check(minSubArraySum):
        assert minSubArraySum([100, -33, 32, -1, 0, -2]) == -33
    check(minSubArraySum)

def test_hidden_suite_case_010():

    def check(minSubArraySum):
        assert minSubArraySum([-10]) == -10, 'This prints if this assert fails 2 (also good for debugging!)'
    check(minSubArraySum)

def test_hidden_suite_case_011():

    def check(minSubArraySum):
        assert minSubArraySum([7]) == 7
    check(minSubArraySum)

def test_hidden_suite_case_012():

    def check(minSubArraySum):
        assert minSubArraySum([1, -1]) == -1
    check(minSubArraySum)
