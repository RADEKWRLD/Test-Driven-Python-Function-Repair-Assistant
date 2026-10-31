from solution import *

def test_public_examples_case_001():

    def check(prime_fib):
        assert prime_fib(1) == 2
    check(prime_fib)

def test_public_examples_case_002():

    def check(prime_fib):
        assert prime_fib(2) == 3
    check(prime_fib)

def test_public_examples_case_003():

    def check(prime_fib):
        assert prime_fib(3) == 5
    check(prime_fib)

def test_public_examples_case_004():

    def check(prime_fib):
        assert prime_fib(4) == 13
    check(prime_fib)

def test_public_examples_case_005():

    def check(prime_fib):
        assert prime_fib(5) == 89
    check(prime_fib)
