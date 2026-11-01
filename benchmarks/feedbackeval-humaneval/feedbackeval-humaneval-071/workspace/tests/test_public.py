from solution import *

def test_public_examples_case_001():

    def check(triangle_area):
        assert triangle_area(3, 4, 5) == 6.0, 'This prints if this assert fails 1 (good for debugging!)'
    check(triangle_area)

def test_public_examples_case_002():

    def check(triangle_area):
        assert triangle_area(1, 2, 10) == -1
    check(triangle_area)
