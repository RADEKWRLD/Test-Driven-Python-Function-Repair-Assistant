from solution import *  # noqa: F403


def test_public_examples():
    def check(even_odd_palindrome):
        # Check some simple cases
        assert even_odd_palindrome(12) == (4, 6)
        assert even_odd_palindrome(3) == (1, 2)
    check(even_odd_palindrome)
