from solution import *

def test_hidden_suite_case_001():

    def check(digits):
        assert digits(5) == 5
    check(digits)

def test_hidden_suite_case_002():

    def check(digits):
        assert digits(54) == 5
    check(digits)

def test_hidden_suite_case_003():

    def check(digits):
        assert digits(120) == 1
    check(digits)

def test_hidden_suite_case_004():

    def check(digits):
        assert digits(5014) == 5
    check(digits)

def test_hidden_suite_case_005():

    def check(digits):
        assert digits(98765) == 315
    check(digits)

def test_hidden_suite_case_006():

    def check(digits):
        assert digits(5576543) == 2625
    check(digits)

def test_hidden_suite_case_007():

    def check(digits):
        assert digits(2468) == 0
    check(digits)
