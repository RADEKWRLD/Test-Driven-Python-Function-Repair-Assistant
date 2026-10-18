from solution import *  # noqa: F403


def test_public_examples():
    def check(move_one_ball):
        # Check some simple cases
        assert move_one_ball([3, 4, 5, 1, 2])==True, "This prints if this assert fails 1 (good for debugging!)"
        # Check some edge cases that are easy to work out by hand.
        assert move_one_ball([3, 5, 4, 1, 2])==False, "This prints if this assert fails 2 (also good for debugging!)"
    check(move_one_ball)
