from solution import *  # noqa: F403


def test_public_examples():
    def check(largest_prime_factor):
        assert largest_prime_factor(2048) == 2
        assert largest_prime_factor(13195) == 29
    check(largest_prime_factor)
