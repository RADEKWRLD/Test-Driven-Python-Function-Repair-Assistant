from solution import *  # noqa: F403


def test_public_examples():
    def check(minPath):
        # Check some simple cases
        print
        assert minPath([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 3) == [1, 2, 1]
        assert minPath([[5, 9, 3], [4, 1, 6], [7, 8, 2]], 1) == [1]
    check(minPath)
