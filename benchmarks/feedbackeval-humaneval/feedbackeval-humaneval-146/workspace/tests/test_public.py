from solution import *

def test_public_examples_case_001():

    def check(specialFilter):
        assert specialFilter([15, -73, 14, -15]) == 1
    check(specialFilter)

def test_public_examples_case_002():

    def check(specialFilter):
        assert specialFilter([33, -2, -3, 45, 21, 109]) == 2
    check(specialFilter)
