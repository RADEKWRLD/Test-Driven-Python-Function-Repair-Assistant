from solution import *

def test_hidden_suite_case_001():

    def check(words_in_sentence):
        assert words_in_sentence('This is a test') == 'is'
    check(words_in_sentence)

def test_hidden_suite_case_002():

    def check(words_in_sentence):
        assert words_in_sentence('lets go for swimming') == 'go for'
    check(words_in_sentence)

def test_hidden_suite_case_003():

    def check(words_in_sentence):
        assert words_in_sentence('there is no place available here') == 'there is no place'
    check(words_in_sentence)

def test_hidden_suite_case_004():

    def check(words_in_sentence):
        assert words_in_sentence('Hi I am Hussein') == 'Hi am Hussein'
    check(words_in_sentence)

def test_hidden_suite_case_005():

    def check(words_in_sentence):
        assert words_in_sentence('go for it') == 'go for it'
    check(words_in_sentence)

def test_hidden_suite_case_006():

    def check(words_in_sentence):
        assert words_in_sentence('here') == ''
    check(words_in_sentence)

def test_hidden_suite_case_007():

    def check(words_in_sentence):
        assert words_in_sentence('here is') == 'is'
    check(words_in_sentence)
