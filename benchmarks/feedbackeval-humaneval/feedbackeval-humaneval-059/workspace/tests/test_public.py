from solution import *

def test_public_examples_case_001():

    def check(largest_prime_factor):
        assert largest_prime_factor(2048) == 2
    check(largest_prime_factor)

def test_public_examples_case_002():

    def check(largest_prime_factor):
        assert largest_prime_factor(13195) == 29
    check(largest_prime_factor)
