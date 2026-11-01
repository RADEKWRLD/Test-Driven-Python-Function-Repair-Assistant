from solution import *

def test_hidden_suite_case_001():

    def check(is_nested):
        assert is_nested('[[]]') == True, 'This prints if this assert fails 1 (good for debugging!)'
    check(is_nested)

def test_hidden_suite_case_002():

    def check(is_nested):
        assert is_nested('[]]]]]]][[[[[]') == False
    check(is_nested)

def test_hidden_suite_case_003():

    def check(is_nested):
        assert is_nested('[][]') == False
    check(is_nested)

def test_hidden_suite_case_004():

    def check(is_nested):
        assert is_nested('[]') == False
    check(is_nested)

def test_hidden_suite_case_005():

    def check(is_nested):
        assert is_nested('[[[[]]]]') == True
    check(is_nested)

def test_hidden_suite_case_006():

    def check(is_nested):
        assert is_nested('[]]]]]]]]]]') == False
    check(is_nested)

def test_hidden_suite_case_007():

    def check(is_nested):
        assert is_nested('[][][[]]') == True
    check(is_nested)

def test_hidden_suite_case_008():

    def check(is_nested):
        assert is_nested('[[]') == False
    check(is_nested)

def test_hidden_suite_case_009():

    def check(is_nested):
        assert is_nested('[]]') == False
    check(is_nested)

def test_hidden_suite_case_010():

    def check(is_nested):
        assert is_nested('[[]][[') == True
    check(is_nested)

def test_hidden_suite_case_011():

    def check(is_nested):
        assert is_nested('[[][]]') == True
    check(is_nested)

def test_hidden_suite_case_012():

    def check(is_nested):
        assert is_nested('') == False, 'This prints if this assert fails 2 (also good for debugging!)'
    check(is_nested)

def test_hidden_suite_case_013():

    def check(is_nested):
        assert is_nested('[[[[[[[[') == False
    check(is_nested)

def test_hidden_suite_case_014():

    def check(is_nested):
        assert is_nested(']]]]]]]]') == False
    check(is_nested)
