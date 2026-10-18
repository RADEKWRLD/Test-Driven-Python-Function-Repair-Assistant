from solution import *  # noqa: F403


def test_public_examples():
    def check(prime_fib):
        assert prime_fib(1) == 2
        assert prime_fib(2) == 3
        assert prime_fib(3) == 5
        assert prime_fib(4) == 13
        assert prime_fib(5) == 89
    check(prime_fib)
