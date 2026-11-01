from solution import *

def test_public_examples_case_001():

    def check(correct_bracketing):
        assert correct_bracketing('()')
    check(correct_bracketing)

def test_public_examples_case_002():

    def check(correct_bracketing):
        assert correct_bracketing('(()())')
    check(correct_bracketing)

def test_public_examples_case_003():

    def check(correct_bracketing):
        assert not correct_bracketing(')(()')
    check(correct_bracketing)

def test_public_examples_case_004():

    def check(correct_bracketing):
        assert not correct_bracketing('(')
    check(correct_bracketing)
