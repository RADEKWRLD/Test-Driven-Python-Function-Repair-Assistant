from solution import *  # noqa: F403


def test_public_examples():
    def check(search):
        # manually generated tests
        assert search([4, 1, 2, 2, 3, 1]) == 2
        assert search([1, 2, 2, 3, 3, 3, 4, 4, 4]) == 3
        assert search([5, 5, 4, 4, 4]) == -1
    check(search)
