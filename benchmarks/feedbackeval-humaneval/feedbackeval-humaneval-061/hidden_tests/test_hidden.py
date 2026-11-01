from solution import *

def test_hidden_suite_case_001():

    def check(correct_bracketing):
        assert correct_bracketing('()')
    check(correct_bracketing)

def test_hidden_suite_case_002():

    def check(correct_bracketing):
        assert correct_bracketing('(()())')
    check(correct_bracketing)

def test_hidden_suite_case_003():

    def check(correct_bracketing):
        assert correct_bracketing('()()(()())()')
    check(correct_bracketing)

def test_hidden_suite_case_004():

    def check(correct_bracketing):
        assert correct_bracketing('()()((()()())())(()()(()))')
    check(correct_bracketing)

def test_hidden_suite_case_005():

    def check(correct_bracketing):
        assert not correct_bracketing('((()())))')
    check(correct_bracketing)

def test_hidden_suite_case_006():

    def check(correct_bracketing):
        assert not correct_bracketing(')(()')
    check(correct_bracketing)

def test_hidden_suite_case_007():

    def check(correct_bracketing):
        assert not correct_bracketing('(')
    check(correct_bracketing)

def test_hidden_suite_case_008():

    def check(correct_bracketing):
        assert not correct_bracketing('((((')
    check(correct_bracketing)

def test_hidden_suite_case_009():

    def check(correct_bracketing):
        assert not correct_bracketing(')')
    check(correct_bracketing)

def test_hidden_suite_case_010():

    def check(correct_bracketing):
        assert not correct_bracketing('(()')
    check(correct_bracketing)

def test_hidden_suite_case_011():

    def check(correct_bracketing):
        assert not correct_bracketing('()()(()())())(()')
    check(correct_bracketing)

def test_hidden_suite_case_012():

    def check(correct_bracketing):
        assert not correct_bracketing('()()(()())()))()')
    check(correct_bracketing)
