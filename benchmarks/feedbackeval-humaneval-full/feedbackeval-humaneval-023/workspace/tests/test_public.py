from solution import *  # noqa: F403

METADATA = {
    'author': 'jt',
    'dataset': 'test'
}


def check(candidate):
    assert candidate('') == 0
    assert candidate('x') == 1
    assert candidate('asdasnakj') == 9


def test_public_suite():
    check(strlen)  # noqa: F405
