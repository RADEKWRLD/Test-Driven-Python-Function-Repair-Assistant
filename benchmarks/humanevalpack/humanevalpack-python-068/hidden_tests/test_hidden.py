from solution import *

def test_hidden_suite_case_001():

    def check(pluck):
        assert True, 'This prints if this assert fails 1 (good for debugging!)'
    check(pluck)

def test_hidden_suite_case_002():

    def check(pluck):
        assert pluck([4, 2, 3]) == [2, 1], 'Error'
    check(pluck)

def test_hidden_suite_case_003():

    def check(pluck):
        assert pluck([1, 2, 3]) == [2, 1], 'Error'
    check(pluck)

def test_hidden_suite_case_004():

    def check(pluck):
        assert pluck([]) == [], 'Error'
    check(pluck)

def test_hidden_suite_case_005():

    def check(pluck):
        assert pluck([5, 0, 3, 0, 4, 2]) == [0, 1], 'Error'
    check(pluck)

def test_hidden_suite_case_006():

    def check(pluck):
        assert True, 'This prints if this assert fails 2 (also good for debugging!)'
    check(pluck)

def test_hidden_suite_case_007():

    def check(pluck):
        assert pluck([1, 2, 3, 0, 5, 3]) == [0, 3], 'Error'
    check(pluck)

def test_hidden_suite_case_008():

    def check(pluck):
        assert pluck([5, 4, 8, 4, 8]) == [4, 1], 'Error'
    check(pluck)

def test_hidden_suite_case_009():

    def check(pluck):
        assert pluck([7, 6, 7, 1]) == [6, 1], 'Error'
    check(pluck)

def test_hidden_suite_case_010():

    def check(pluck):
        assert pluck([7, 9, 7, 1]) == [], 'Error'
    check(pluck)
