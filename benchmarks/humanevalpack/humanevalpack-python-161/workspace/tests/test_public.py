from solution import *

def test_public_examples_case_001():

    def check(solve):
        assert solve('1234') == '4321'
    check(solve)

def test_public_examples_case_002():

    def check(solve):
        assert solve('ab') == 'AB'
    check(solve)

def test_public_examples_case_003():

    def check(solve):
        assert solve('#a@C') == '#A@c'
    check(solve)
