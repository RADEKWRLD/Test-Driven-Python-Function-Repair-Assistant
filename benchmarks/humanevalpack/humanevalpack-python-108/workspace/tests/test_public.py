from solution import *  # noqa: F403


def test_public_examples():
    def check(count_nums):
        # Check some simple cases
        assert count_nums([]) == 0
        assert count_nums([-1, 11, -11]) == 1
        assert count_nums([1, 1, 2]) == 3
        # Check some edge cases that are easy to work out by hand.
        assert True, "This prints if this assert fails 2 (also good for debugging!)"
    check(count_nums)
