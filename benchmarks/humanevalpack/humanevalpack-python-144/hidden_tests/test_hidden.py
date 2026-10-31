from solution import *

def test_hidden_suite_case_001():

    def check(simplify):
        assert simplify('1/5', '5/1') == True, 'test1'
    check(simplify)

def test_hidden_suite_case_002():

    def check(simplify):
        assert simplify('1/6', '2/1') == False, 'test2'
    check(simplify)

def test_hidden_suite_case_003():

    def check(simplify):
        assert simplify('5/1', '3/1') == True, 'test3'
    check(simplify)

def test_hidden_suite_case_004():

    def check(simplify):
        assert simplify('7/10', '10/2') == False, 'test4'
    check(simplify)

def test_hidden_suite_case_005():

    def check(simplify):
        assert simplify('2/10', '50/10') == True, 'test5'
    check(simplify)

def test_hidden_suite_case_006():

    def check(simplify):
        assert simplify('7/2', '4/2') == True, 'test6'
    check(simplify)

def test_hidden_suite_case_007():

    def check(simplify):
        assert simplify('11/6', '6/1') == True, 'test7'
    check(simplify)

def test_hidden_suite_case_008():

    def check(simplify):
        assert simplify('2/3', '5/2') == False, 'test8'
    check(simplify)

def test_hidden_suite_case_009():

    def check(simplify):
        assert simplify('5/2', '3/5') == False, 'test9'
    check(simplify)

def test_hidden_suite_case_010():

    def check(simplify):
        assert simplify('2/4', '8/4') == True, 'test10'
    check(simplify)

def test_hidden_suite_case_011():

    def check(simplify):
        assert simplify('2/4', '4/2') == True, 'test11'
    check(simplify)

def test_hidden_suite_case_012():

    def check(simplify):
        assert simplify('1/5', '5/1') == True, 'test12'
    check(simplify)

def test_hidden_suite_case_013():

    def check(simplify):
        assert simplify('1/5', '1/5') == False, 'test13'
    check(simplify)
