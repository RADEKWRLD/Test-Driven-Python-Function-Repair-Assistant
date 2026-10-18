from solution import *  # noqa: F403


def test_public_examples():
    def check(fizz_buzz):
        assert fizz_buzz(50) == 0
        assert fizz_buzz(78) == 2
        assert fizz_buzz(79) == 3
    check(fizz_buzz)
