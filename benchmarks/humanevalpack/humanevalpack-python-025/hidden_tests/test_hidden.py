from solution import *

def test_hidden_suite_case_001():

    def check(factorize):
        assert factorize(2) == [2]
    check(factorize)

def test_hidden_suite_case_002():

    def check(factorize):
        assert factorize(4) == [2, 2]
    check(factorize)

def test_hidden_suite_case_003():

    def check(factorize):
        assert factorize(8) == [2, 2, 2]
    check(factorize)

def test_hidden_suite_case_004():

    def check(factorize):
        assert factorize(3 * 19) == [3, 19]
    check(factorize)

def test_hidden_suite_case_005():

    def check(factorize):
        assert factorize(3 * 19 * 3 * 19) == [3, 3, 19, 19]
    check(factorize)

def test_hidden_suite_case_006():

    def check(factorize):
        assert factorize(3 * 19 * 3 * 19 * 3 * 19) == [3, 3, 3, 19, 19, 19]
    check(factorize)

def test_hidden_suite_case_007():

    def check(factorize):
        assert factorize(3 * 19 * 19 * 19) == [3, 19, 19, 19]
    check(factorize)

def test_hidden_suite_case_008():

    def check(factorize):
        assert factorize(3 * 2 * 3) == [2, 3, 3]
    check(factorize)
