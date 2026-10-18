from solution import *  # noqa: F403


def test_public_examples():
    def check(intersection):
        # Check some simple cases
        assert intersection((1, 2), (2, 3)) == "NO"
        assert intersection((-1, 1), (0, 4)) == "NO"
        assert intersection((-3, -1), (-5, 5)) == "YES"
    check(intersection)
