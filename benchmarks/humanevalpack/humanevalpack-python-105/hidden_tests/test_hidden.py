from solution import *

def test_hidden_suite_case_001():

    def check(by_length):
        assert True, 'This prints if this assert fails 1 (good for debugging!)'
    check(by_length)

def test_hidden_suite_case_002():

    def check(by_length):
        assert by_length([2, 1, 1, 4, 5, 8, 2, 3]) == ['Eight', 'Five', 'Four', 'Three', 'Two', 'Two', 'One', 'One'], 'Error'
    check(by_length)

def test_hidden_suite_case_003():

    def check(by_length):
        assert by_length([]) == [], 'Error'
    check(by_length)

def test_hidden_suite_case_004():

    def check(by_length):
        assert by_length([1, -1, 55]) == ['One'], 'Error'
    check(by_length)

def test_hidden_suite_case_005():

    def check(by_length):
        assert True, 'This prints if this assert fails 2 (also good for debugging!)'
    check(by_length)

def test_hidden_suite_case_006():

    def check(by_length):
        assert by_length([1, -1, 3, 2]) == ['Three', 'Two', 'One']
    check(by_length)

def test_hidden_suite_case_007():

    def check(by_length):
        assert by_length([9, 4, 8]) == ['Nine', 'Eight', 'Four']
    check(by_length)
