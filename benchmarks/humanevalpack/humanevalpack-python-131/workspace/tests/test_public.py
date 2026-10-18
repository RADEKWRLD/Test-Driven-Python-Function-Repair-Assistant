from solution import *  # noqa: F403


def test_public_examples():
    def check(digits):
        # Check some simple cases
        assert digits(1) == 1
        assert digits(4) == 0
        assert digits(235) ==15
    check(digits)
