from solution import *  # noqa: F403

METADATA = {}


def check(candidate):
    assert candidate(15) == 5
    assert candidate(27) == 3
    assert candidate(63) == 7
    assert candidate(330) == 11
    assert candidate(13195) == 29


def test_public_suite():
    check(largest_prime_factor)  # noqa: F405
