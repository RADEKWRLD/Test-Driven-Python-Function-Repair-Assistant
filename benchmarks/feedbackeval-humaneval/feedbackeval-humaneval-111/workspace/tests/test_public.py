from solution import *

def test_public_examples_case_001():

    def check(histogram):
        assert histogram('a b b a') == {'a': 2, 'b': 2}, 'This prints if this assert fails 1 (good for debugging!)'
    check(histogram)

def test_public_examples_case_002():

    def check(histogram):
        assert histogram('a b c a b') == {'a': 2, 'b': 2}, 'This prints if this assert fails 2 (good for debugging!)'
    check(histogram)

def test_public_examples_case_003():

    def check(histogram):
        assert histogram('a b c') == {'a': 1, 'b': 1, 'c': 1}, 'This prints if this assert fails 4 (good for debugging!)'
    check(histogram)

def test_public_examples_case_004():

    def check(histogram):
        assert histogram('b b b b a') == {'b': 4}, 'This prints if this assert fails 5 (good for debugging!)'
    check(histogram)

def test_public_examples_case_005():

    def check(histogram):
        assert histogram('') == {}, 'This prints if this assert fails 7 (also good for debugging!)'
    check(histogram)
