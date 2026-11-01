from solution import *

def test_public_examples_case_001():

    def check(simplify):
        assert simplify('1/5', '5/1') == True, 'test1'
    check(simplify)

def test_public_examples_case_002():

    def check(simplify):
        assert simplify('1/6', '2/1') == False, 'test2'
    check(simplify)

def test_public_examples_case_003():

    def check(simplify):
        assert simplify('7/10', '10/2') == False, 'test4'
    check(simplify)
