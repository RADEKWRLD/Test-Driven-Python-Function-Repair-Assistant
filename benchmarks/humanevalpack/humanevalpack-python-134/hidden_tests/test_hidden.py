from solution import *

def test_hidden_suite_case_001():

    def check(check_if_last_char_is_a_letter):
        assert check_if_last_char_is_a_letter('apple') == False
    check(check_if_last_char_is_a_letter)

def test_hidden_suite_case_002():

    def check(check_if_last_char_is_a_letter):
        assert check_if_last_char_is_a_letter('apple pi e') == True
    check(check_if_last_char_is_a_letter)

def test_hidden_suite_case_003():

    def check(check_if_last_char_is_a_letter):
        assert check_if_last_char_is_a_letter('eeeee') == False
    check(check_if_last_char_is_a_letter)

def test_hidden_suite_case_004():

    def check(check_if_last_char_is_a_letter):
        assert check_if_last_char_is_a_letter('A') == True
    check(check_if_last_char_is_a_letter)

def test_hidden_suite_case_005():

    def check(check_if_last_char_is_a_letter):
        assert check_if_last_char_is_a_letter('Pumpkin pie ') == False
    check(check_if_last_char_is_a_letter)

def test_hidden_suite_case_006():

    def check(check_if_last_char_is_a_letter):
        assert check_if_last_char_is_a_letter('Pumpkin pie 1') == False
    check(check_if_last_char_is_a_letter)

def test_hidden_suite_case_007():

    def check(check_if_last_char_is_a_letter):
        assert check_if_last_char_is_a_letter('') == False
    check(check_if_last_char_is_a_letter)

def test_hidden_suite_case_008():

    def check(check_if_last_char_is_a_letter):
        assert check_if_last_char_is_a_letter('eeeee e ') == False
    check(check_if_last_char_is_a_letter)

def test_hidden_suite_case_009():

    def check(check_if_last_char_is_a_letter):
        assert check_if_last_char_is_a_letter('apple pie') == False
    check(check_if_last_char_is_a_letter)

def test_hidden_suite_case_010():

    def check(check_if_last_char_is_a_letter):
        assert check_if_last_char_is_a_letter('apple pi e ') == False
    check(check_if_last_char_is_a_letter)

def test_hidden_suite_case_011():

    def check(check_if_last_char_is_a_letter):
        assert True
    check(check_if_last_char_is_a_letter)
