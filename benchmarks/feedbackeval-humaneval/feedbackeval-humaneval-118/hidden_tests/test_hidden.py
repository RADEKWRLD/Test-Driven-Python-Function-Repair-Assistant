from solution import *

def test_hidden_suite_case_001():

    def check(get_closest_vowel):
        assert get_closest_vowel('yogurt') == 'u'
    check(get_closest_vowel)

def test_hidden_suite_case_002():

    def check(get_closest_vowel):
        assert get_closest_vowel('full') == 'u'
    check(get_closest_vowel)

def test_hidden_suite_case_003():

    def check(get_closest_vowel):
        assert get_closest_vowel('easy') == ''
    check(get_closest_vowel)

def test_hidden_suite_case_004():

    def check(get_closest_vowel):
        assert get_closest_vowel('eAsy') == ''
    check(get_closest_vowel)

def test_hidden_suite_case_005():

    def check(get_closest_vowel):
        assert get_closest_vowel('ali') == ''
    check(get_closest_vowel)

def test_hidden_suite_case_006():

    def check(get_closest_vowel):
        assert get_closest_vowel('bad') == 'a'
    check(get_closest_vowel)

def test_hidden_suite_case_007():

    def check(get_closest_vowel):
        assert get_closest_vowel('most') == 'o'
    check(get_closest_vowel)

def test_hidden_suite_case_008():

    def check(get_closest_vowel):
        assert get_closest_vowel('ab') == ''
    check(get_closest_vowel)

def test_hidden_suite_case_009():

    def check(get_closest_vowel):
        assert get_closest_vowel('ba') == ''
    check(get_closest_vowel)

def test_hidden_suite_case_010():

    def check(get_closest_vowel):
        assert get_closest_vowel('quick') == ''
    check(get_closest_vowel)

def test_hidden_suite_case_011():

    def check(get_closest_vowel):
        assert get_closest_vowel('anime') == 'i'
    check(get_closest_vowel)

def test_hidden_suite_case_012():

    def check(get_closest_vowel):
        assert get_closest_vowel('Asia') == ''
    check(get_closest_vowel)

def test_hidden_suite_case_013():

    def check(get_closest_vowel):
        assert get_closest_vowel('Above') == 'o'
    check(get_closest_vowel)

def test_hidden_suite_case_014():

    def check(get_closest_vowel):
        assert True
    check(get_closest_vowel)
