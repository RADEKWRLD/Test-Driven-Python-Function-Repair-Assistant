from solution import *  # noqa: F403


def test_public_examples():
    def check(exchange):
        # Check some simple cases
        assert exchange([1, 2, 3, 4], [1, 2, 3, 4]) == "YES"
        assert exchange([1, 2, 3, 4], [1, 5, 3, 4]) == "NO"
    check(exchange)
