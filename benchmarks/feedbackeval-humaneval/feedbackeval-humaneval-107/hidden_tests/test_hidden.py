from solution import *

def test_hidden_suite_case_001():

    def check(even_odd_palindrome):
        assert even_odd_palindrome(123) == (8, 13)
    check(even_odd_palindrome)

def test_hidden_suite_case_002():

    def check(even_odd_palindrome):
        assert even_odd_palindrome(12) == (4, 6)
    check(even_odd_palindrome)

def test_hidden_suite_case_003():

    def check(even_odd_palindrome):
        assert even_odd_palindrome(3) == (1, 2)
    check(even_odd_palindrome)

def test_hidden_suite_case_004():

    def check(even_odd_palindrome):
        assert even_odd_palindrome(63) == (6, 8)
    check(even_odd_palindrome)

def test_hidden_suite_case_005():

    def check(even_odd_palindrome):
        assert even_odd_palindrome(25) == (5, 6)
    check(even_odd_palindrome)

def test_hidden_suite_case_006():

    def check(even_odd_palindrome):
        assert even_odd_palindrome(19) == (4, 6)
    check(even_odd_palindrome)

def test_hidden_suite_case_007():

    def check(even_odd_palindrome):
        assert even_odd_palindrome(9) == (4, 5), 'This prints if this assert fails 1 (good for debugging!)'
    check(even_odd_palindrome)

def test_hidden_suite_case_008():

    def check(even_odd_palindrome):
        assert even_odd_palindrome(1) == (0, 1), 'This prints if this assert fails 2 (also good for debugging!)'
    check(even_odd_palindrome)
