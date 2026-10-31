from solution import *

def test_public_examples_case_001():

    def check(get_closest_vowel):
        assert get_closest_vowel('yogurt') == 'u'
    check(get_closest_vowel)

def test_public_examples_case_002():

    def check(get_closest_vowel):
        assert get_closest_vowel('FULL') == 'U'
    check(get_closest_vowel)

def test_public_examples_case_003():

    def check(get_closest_vowel):
        assert get_closest_vowel('ab') == ''
    check(get_closest_vowel)

def test_public_examples_case_004():

    def check(get_closest_vowel):
        assert get_closest_vowel('quick') == ''
    check(get_closest_vowel)
