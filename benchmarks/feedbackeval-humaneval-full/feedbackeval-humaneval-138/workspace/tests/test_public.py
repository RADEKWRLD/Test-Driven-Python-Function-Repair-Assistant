from solution import *  # noqa: F403

def check(candidate):
    assert candidate(4) == False
    assert candidate(6) == False
    assert candidate(8) == True
    assert candidate(10) == True
    assert candidate(11) == False
    assert candidate(12) == True
    assert candidate(13) == False
    assert candidate(16) == True


def test_public_suite():
    check(is_equal_to_sum_even)  # noqa: F405
