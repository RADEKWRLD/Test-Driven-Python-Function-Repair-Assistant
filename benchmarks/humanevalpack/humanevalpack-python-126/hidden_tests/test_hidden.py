from solution import *

def test_hidden_suite_case_001():

    def check(is_sorted):
        assert is_sorted([5]) == True
    check(is_sorted)

def test_hidden_suite_case_002():

    def check(is_sorted):
        assert is_sorted([1, 2, 3, 4, 5]) == True
    check(is_sorted)

def test_hidden_suite_case_003():

    def check(is_sorted):
        assert is_sorted([1, 3, 2, 4, 5]) == False
    check(is_sorted)

def test_hidden_suite_case_004():

    def check(is_sorted):
        assert is_sorted([1, 2, 3, 4, 5, 6]) == True
    check(is_sorted)

def test_hidden_suite_case_005():

    def check(is_sorted):
        assert is_sorted([1, 2, 3, 4, 5, 6, 7]) == True
    check(is_sorted)

def test_hidden_suite_case_006():

    def check(is_sorted):
        assert is_sorted([1, 3, 2, 4, 5, 6, 7]) == False, 'This prints if this assert fails 1 (good for debugging!)'
    check(is_sorted)

def test_hidden_suite_case_007():

    def check(is_sorted):
        assert is_sorted([]) == True, 'This prints if this assert fails 2 (good for debugging!)'
    check(is_sorted)

def test_hidden_suite_case_008():

    def check(is_sorted):
        assert is_sorted([1]) == True, 'This prints if this assert fails 3 (good for debugging!)'
    check(is_sorted)

def test_hidden_suite_case_009():

    def check(is_sorted):
        assert is_sorted([3, 2, 1]) == False, 'This prints if this assert fails 4 (good for debugging!)'
    check(is_sorted)

def test_hidden_suite_case_010():

    def check(is_sorted):
        assert is_sorted([1, 2, 2, 2, 3, 4]) == False, 'This prints if this assert fails 5 (good for debugging!)'
    check(is_sorted)

def test_hidden_suite_case_011():

    def check(is_sorted):
        assert is_sorted([1, 2, 3, 3, 3, 4]) == False, 'This prints if this assert fails 6 (good for debugging!)'
    check(is_sorted)

def test_hidden_suite_case_012():

    def check(is_sorted):
        assert is_sorted([1, 2, 2, 3, 3, 4]) == True, 'This prints if this assert fails 7 (good for debugging!)'
    check(is_sorted)

def test_hidden_suite_case_013():

    def check(is_sorted):
        assert is_sorted([1, 2, 3, 4]) == True, 'This prints if this assert fails 8 (good for debugging!)'
    check(is_sorted)
