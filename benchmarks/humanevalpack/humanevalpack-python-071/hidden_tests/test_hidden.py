from solution import *

def test_hidden_suite_case_001():

    def check(triangle_area):
        assert triangle_area(3, 4, 5) == 6.0, 'This prints if this assert fails 1 (good for debugging!)'
    check(triangle_area)

def test_hidden_suite_case_002():

    def check(triangle_area):
        assert triangle_area(1, 2, 10) == -1
    check(triangle_area)

def test_hidden_suite_case_003():

    def check(triangle_area):
        assert triangle_area(4, 8, 5) == 8.18
    check(triangle_area)

def test_hidden_suite_case_004():

    def check(triangle_area):
        assert triangle_area(2, 2, 2) == 1.73
    check(triangle_area)

def test_hidden_suite_case_005():

    def check(triangle_area):
        assert triangle_area(1, 2, 3) == -1
    check(triangle_area)

def test_hidden_suite_case_006():

    def check(triangle_area):
        assert triangle_area(10, 5, 7) == 16.25
    check(triangle_area)

def test_hidden_suite_case_007():

    def check(triangle_area):
        assert triangle_area(2, 6, 3) == -1
    check(triangle_area)

def test_hidden_suite_case_008():

    def check(triangle_area):
        assert triangle_area(1, 1, 1) == 0.43, 'This prints if this assert fails 2 (also good for debugging!)'
    check(triangle_area)

def test_hidden_suite_case_009():

    def check(triangle_area):
        assert triangle_area(2, 2, 10) == -1
    check(triangle_area)
