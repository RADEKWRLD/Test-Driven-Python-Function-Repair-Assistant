from solution import *  # noqa: F403


def test_public_examples():
    def check(order_by_points):
        # Check some simple cases
        assert order_by_points([1, 11, -1, -11, -12]) == [-1, -11, 1, -12, 11]
        assert order_by_points([]) == []
    check(order_by_points)
