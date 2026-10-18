from solution import *  # noqa: F403


def test_public_examples():
    def check(triangle_area):
        # Check some simple cases
        assert triangle_area(3, 4, 5) == 6.00, "This prints if this assert fails 1 (good for debugging!)"
        assert triangle_area(1, 2, 10) == -1
    check(triangle_area)
