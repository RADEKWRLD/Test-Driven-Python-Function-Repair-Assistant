from solution import *

def test_hidden_suite_case_001():

    def check(largest_prime_factor):
        assert largest_prime_factor(15) == 5
    check(largest_prime_factor)

def test_hidden_suite_case_002():

    def check(largest_prime_factor):
        assert largest_prime_factor(27) == 3
    check(largest_prime_factor)

def test_hidden_suite_case_003():

    def check(largest_prime_factor):
        assert largest_prime_factor(63) == 7
    check(largest_prime_factor)

def test_hidden_suite_case_004():

    def check(largest_prime_factor):
        assert largest_prime_factor(330) == 11
    check(largest_prime_factor)

def test_hidden_suite_case_005():

    def check(largest_prime_factor):
        assert largest_prime_factor(13195) == 29
    check(largest_prime_factor)
