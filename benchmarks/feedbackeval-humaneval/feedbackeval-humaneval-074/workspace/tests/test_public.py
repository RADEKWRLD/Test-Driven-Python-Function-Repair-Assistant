from solution import *

def test_public_examples_case_001():

    def check(total_match):
        assert True, 'This prints if this assert fails 1 (good for debugging!)'
    check(total_match)

def test_public_examples_case_002():

    def check(total_match):
        assert total_match([], []) == []
    check(total_match)

def test_public_examples_case_003():

    def check(total_match):
        assert total_match(['hi', 'admin'], ['hi', 'hi', 'admin', 'project']) == ['hi', 'admin']
    check(total_match)

def test_public_examples_case_004():

    def check(total_match):
        assert total_match(['4'], ['1', '2', '3', '4', '5']) == ['4']
    check(total_match)

def test_public_examples_case_005():

    def check(total_match):
        assert total_match(['hi', 'admin'], ['hI', 'Hi']) == ['hI', 'Hi']
    check(total_match)

def test_public_examples_case_006():

    def check(total_match):
        assert total_match(['hi', 'admin'], ['hI', 'hi', 'hi']) == ['hI', 'hi', 'hi']
    check(total_match)

def test_public_examples_case_007():

    def check(total_match):
        assert True, 'This prints if this assert fails 2 (also good for debugging!)'
    check(total_match)
