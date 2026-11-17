from solution import *  # noqa: F403

def check(candidate):

    assert candidate(5) == 1
    assert candidate(6) == 4
    assert candidate(10) == 36
    assert candidate(100) == 53361


def test_public_suite():
    check(get_max_triples)  # noqa: F405
