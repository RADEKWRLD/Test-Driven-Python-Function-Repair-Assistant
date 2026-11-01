from solution import *

def test_public_examples_case_001():

    def check(check_if_last_char_is_a_letter):
        assert check_if_last_char_is_a_letter('apple pi e') == True
    check(check_if_last_char_is_a_letter)

def test_public_examples_case_002():

    def check(check_if_last_char_is_a_letter):
        assert check_if_last_char_is_a_letter('') == False
    check(check_if_last_char_is_a_letter)

def test_public_examples_case_003():

    def check(check_if_last_char_is_a_letter):
        assert check_if_last_char_is_a_letter('apple pie') == False
    check(check_if_last_char_is_a_letter)

def test_public_examples_case_004():

    def check(check_if_last_char_is_a_letter):
        assert check_if_last_char_is_a_letter('apple pi e ') == False
    check(check_if_last_char_is_a_letter)

def test_public_examples_case_005():

    def check(check_if_last_char_is_a_letter):
        assert True
    check(check_if_last_char_is_a_letter)
