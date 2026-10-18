from solution import *  # noqa: F403


def test_public_examples():
    def check(sum_squares):
        # Check some simple cases
        assert sum_squares([1,2,3]) == 6
        assert sum_squares([]) == 0
        assert sum_squares([-1,-5,2,-1,-5]) == -126
        # Don't remove this line:
    check(sum_squares)
