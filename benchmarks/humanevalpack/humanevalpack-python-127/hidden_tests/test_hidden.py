from solution import *

def test_hidden_suite_case_001():

    def check(intersection):
        assert intersection((1, 2), (2, 3)) == 'NO'
    check(intersection)

def test_hidden_suite_case_002():

    def check(intersection):
        assert intersection((-1, 1), (0, 4)) == 'NO'
    check(intersection)

def test_hidden_suite_case_003():

    def check(intersection):
        assert intersection((-3, -1), (-5, 5)) == 'YES'
    check(intersection)

def test_hidden_suite_case_004():

    def check(intersection):
        assert intersection((-2, 2), (-4, 0)) == 'YES'
    check(intersection)

def test_hidden_suite_case_005():

    def check(intersection):
        assert intersection((-11, 2), (-1, -1)) == 'NO'
    check(intersection)

def test_hidden_suite_case_006():

    def check(intersection):
        assert intersection((1, 2), (3, 5)) == 'NO'
    check(intersection)

def test_hidden_suite_case_007():

    def check(intersection):
        assert intersection((1, 2), (1, 2)) == 'NO'
    check(intersection)

def test_hidden_suite_case_008():

    def check(intersection):
        assert intersection((-2, -2), (-3, -2)) == 'NO'
    check(intersection)
