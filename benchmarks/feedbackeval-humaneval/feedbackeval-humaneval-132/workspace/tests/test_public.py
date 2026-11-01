from solution import *

def test_public_examples_case_001():

    def check(is_nested):
        assert is_nested('[[]]') == True, 'This prints if this assert fails 1 (good for debugging!)'
    check(is_nested)

def test_public_examples_case_002():

    def check(is_nested):
        assert is_nested('[]]]]]]][[[[[]') == False
    check(is_nested)

def test_public_examples_case_003():

    def check(is_nested):
        assert is_nested('[][]') == False
    check(is_nested)

def test_public_examples_case_004():

    def check(is_nested):
        assert is_nested('[]') == False
    check(is_nested)

def test_public_examples_case_005():

    def check(is_nested):
        assert is_nested('[[]][[') == True
    check(is_nested)

def test_public_examples_case_006():

    def check(is_nested):
        assert is_nested('[[][]]') == True
    check(is_nested)
