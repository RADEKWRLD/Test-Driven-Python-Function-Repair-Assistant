from solution import *

def test_public_examples_case_001():

    def check(fizz_buzz):
        assert fizz_buzz(50) == 0
    check(fizz_buzz)

def test_public_examples_case_002():

    def check(fizz_buzz):
        assert fizz_buzz(78) == 2
    check(fizz_buzz)

def test_public_examples_case_003():

    def check(fizz_buzz):
        assert fizz_buzz(79) == 3
    check(fizz_buzz)
