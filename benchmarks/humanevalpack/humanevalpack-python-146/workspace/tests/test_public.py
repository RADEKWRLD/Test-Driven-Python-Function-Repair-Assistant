from solution import *  # noqa: F403


def test_public_examples():
    def check(specialFilter):
        # Check some simple cases 
        assert specialFilter([15, -73, 14, -15]) == 1
        assert specialFilter([33, -2, -3, 45, 21, 109]) == 2
    check(specialFilter)
