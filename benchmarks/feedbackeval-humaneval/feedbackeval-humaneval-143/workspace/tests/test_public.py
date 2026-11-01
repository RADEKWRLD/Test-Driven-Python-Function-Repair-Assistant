from solution import *

def test_public_examples_case_001():

    def check(words_in_sentence):
        assert words_in_sentence('This is a test') == 'is'
    check(words_in_sentence)

def test_public_examples_case_002():

    def check(words_in_sentence):
        assert words_in_sentence('lets go for swimming') == 'go for'
    check(words_in_sentence)
