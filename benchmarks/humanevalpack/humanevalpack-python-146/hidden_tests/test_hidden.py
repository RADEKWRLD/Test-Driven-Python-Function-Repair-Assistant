from solution import *

def test_hidden_suite_case_001():

    def check(specialFilter):
        assert specialFilter([5, -2, 1, -5]) == 0
    check(specialFilter)

def test_hidden_suite_case_002():

    def check(specialFilter):
        assert specialFilter([15, -73, 14, -15]) == 1
    check(specialFilter)

def test_hidden_suite_case_003():

    def check(specialFilter):
        assert specialFilter([33, -2, -3, 45, 21, 109]) == 2
    check(specialFilter)

def test_hidden_suite_case_004():

    def check(specialFilter):
        assert specialFilter([43, -12, 93, 125, 121, 109]) == 4
    check(specialFilter)

def test_hidden_suite_case_005():

    def check(specialFilter):
        assert specialFilter([71, -2, -33, 75, 21, 19]) == 3
    check(specialFilter)

def test_hidden_suite_case_006():

    def check(specialFilter):
        assert specialFilter([1]) == 0
    check(specialFilter)

def test_hidden_suite_case_007():

    def check(specialFilter):
        assert specialFilter([]) == 0
    check(specialFilter)
