from solution import *  # noqa: F403


def test_public_examples():
    def check(factorize):
        assert factorize(8) == [2, 2, 2]
        assert factorize(25) == [5,5]
        assert factorize(70) == [2,5,7]
    check(factorize)
