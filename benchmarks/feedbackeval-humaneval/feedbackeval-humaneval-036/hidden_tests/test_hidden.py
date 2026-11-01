from solution import *

def test_hidden_suite_case_001():

    def check(fizz_buzz):
        assert fizz_buzz(50) == 0
    check(fizz_buzz)

def test_hidden_suite_case_002():

    def check(fizz_buzz):
        assert fizz_buzz(78) == 2
    check(fizz_buzz)

def test_hidden_suite_case_003():

    def check(fizz_buzz):
        assert fizz_buzz(79) == 3
    check(fizz_buzz)

def test_hidden_suite_case_004():

    def check(fizz_buzz):
        assert fizz_buzz(100) == 3
    check(fizz_buzz)

def test_hidden_suite_case_005():

    def check(fizz_buzz):
        assert fizz_buzz(200) == 6
    check(fizz_buzz)

def test_hidden_suite_case_006():

    def check(fizz_buzz):
        assert fizz_buzz(4000) == 192
    check(fizz_buzz)

def test_hidden_suite_case_007():

    def check(fizz_buzz):
        assert fizz_buzz(10000) == 639
    check(fizz_buzz)

def test_hidden_suite_case_008():

    def check(fizz_buzz):
        assert fizz_buzz(100000) == 8026
    check(fizz_buzz)
