from solution import *

def test_public_examples_case_001():

    def check(minSubArraySum):
        assert minSubArraySum([2, 3, 4, 1, 2, 4]) == 1, 'This prints if this assert fails 1 (good for debugging!)'
    check(minSubArraySum)

def test_public_examples_case_002():

    def check(minSubArraySum):
        assert minSubArraySum([-1, -2, -3]) == -6
    check(minSubArraySum)
