from solution import *  # noqa: F403


def test_public_examples():
    def check(will_it_fly):
        # Check some simple cases
        assert will_it_fly([3, 2, 3], 9) is True
        assert will_it_fly([1, 2], 5) is False
        assert will_it_fly([3], 5) is True
        assert will_it_fly([3, 2, 3], 1) is False
    check(will_it_fly)
