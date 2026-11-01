from solution import *

def test_hidden_suite_case_001():

    def check(compare_one):
        assert compare_one(1, 2) == 2
    check(compare_one)

def test_hidden_suite_case_002():

    def check(compare_one):
        assert compare_one(1, 2.5) == 2.5
    check(compare_one)

def test_hidden_suite_case_003():

    def check(compare_one):
        assert compare_one(2, 3) == 3
    check(compare_one)

def test_hidden_suite_case_004():

    def check(compare_one):
        assert compare_one(5, 6) == 6
    check(compare_one)

def test_hidden_suite_case_005():

    def check(compare_one):
        assert compare_one(1, '2,3') == '2,3'
    check(compare_one)

def test_hidden_suite_case_006():

    def check(compare_one):
        assert compare_one('5,1', '6') == '6'
    check(compare_one)

def test_hidden_suite_case_007():

    def check(compare_one):
        assert compare_one('1', '2') == '2'
    check(compare_one)

def test_hidden_suite_case_008():

    def check(compare_one):
        assert compare_one('1', 1) == None
    check(compare_one)

def test_hidden_suite_case_009():

    def check(compare_one):
        assert True
    check(compare_one)
