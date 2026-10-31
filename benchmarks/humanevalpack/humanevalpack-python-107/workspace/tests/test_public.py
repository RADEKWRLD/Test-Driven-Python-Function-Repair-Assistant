from solution import *

def test_public_examples_case_001():

    def check(even_odd_palindrome):
        assert even_odd_palindrome(12) == (4, 6)
    check(even_odd_palindrome)

def test_public_examples_case_002():

    def check(even_odd_palindrome):
        assert even_odd_palindrome(3) == (1, 2)
    check(even_odd_palindrome)
