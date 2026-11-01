from solution import *  # noqa: F403

METADATA = {}


def check(candidate):
    assert candidate(1) == 1
    assert candidate(6) == 21
    assert candidate(11) == 66
    assert candidate(30) == 465
    assert candidate(100) == 5050


def test_public_suite():
    check(sum_to_n)  # noqa: F405
