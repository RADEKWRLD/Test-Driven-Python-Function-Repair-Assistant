from solution import *  # noqa: F403


def test_public_examples():
    def check(minSubArraySum):
        # Check some simple cases
        assert minSubArraySum([2, 3, 4, 1, 2, 4]) == 1, "This prints if this assert fails 1 (good for debugging!)"
        assert minSubArraySum([-1, -2, -3]) == -6
    check(minSubArraySum)
