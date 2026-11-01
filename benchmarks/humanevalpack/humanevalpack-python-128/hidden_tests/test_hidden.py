from solution import *

def test_hidden_suite_case_001():

    def check(prod_signs):
        assert True, 'This prints if this assert fails 1 (good for debugging!)'
    check(prod_signs)

def test_hidden_suite_case_002():

    def check(prod_signs):
        assert prod_signs([1, 2, 2, -4]) == -9
    check(prod_signs)

def test_hidden_suite_case_003():

    def check(prod_signs):
        assert prod_signs([0, 1]) == 0
    check(prod_signs)

def test_hidden_suite_case_004():

    def check(prod_signs):
        assert prod_signs([1, 1, 1, 2, 3, -1, 1]) == -10
    check(prod_signs)

def test_hidden_suite_case_005():

    def check(prod_signs):
        assert prod_signs([]) == None
    check(prod_signs)

def test_hidden_suite_case_006():

    def check(prod_signs):
        assert prod_signs([2, 4, 1, 2, -1, -1, 9]) == 20
    check(prod_signs)

def test_hidden_suite_case_007():

    def check(prod_signs):
        assert prod_signs([-1, 1, -1, 1]) == 4
    check(prod_signs)

def test_hidden_suite_case_008():

    def check(prod_signs):
        assert prod_signs([-1, 1, 1, 1]) == -4
    check(prod_signs)

def test_hidden_suite_case_009():

    def check(prod_signs):
        assert prod_signs([-1, 1, 1, 0]) == 0
    check(prod_signs)

def test_hidden_suite_case_010():

    def check(prod_signs):
        assert True, 'This prints if this assert fails 2 (also good for debugging!)'
    check(prod_signs)
