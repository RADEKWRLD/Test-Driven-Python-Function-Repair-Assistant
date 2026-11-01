from solution import *  # noqa: F403

METADATA = {}


def check(candidate):
    assert candidate([1, 2, 3]) == 3
    assert candidate([5, 3, -5, 2, -3, 3, 9, 0, 124, 1, -10]) == 124


def test_public_suite():
    check(max_element)  # noqa: F405
