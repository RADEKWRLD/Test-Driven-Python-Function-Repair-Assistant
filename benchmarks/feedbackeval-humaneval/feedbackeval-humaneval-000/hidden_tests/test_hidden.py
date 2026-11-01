from solution import *

def test_hidden_suite_case_001():

    def check(has_close_elements):
        assert has_close_elements([1.0, 2.0, 3.9, 4.0, 5.0, 2.2], 0.3) == True
    check(has_close_elements)

def test_hidden_suite_case_002():

    def check(has_close_elements):
        assert has_close_elements([1.0, 2.0, 3.9, 4.0, 5.0, 2.2], 0.05) == False
    check(has_close_elements)

def test_hidden_suite_case_003():

    def check(has_close_elements):
        assert has_close_elements([1.0, 2.0, 5.9, 4.0, 5.0], 0.95) == True
    check(has_close_elements)

def test_hidden_suite_case_004():

    def check(has_close_elements):
        assert has_close_elements([1.0, 2.0, 5.9, 4.0, 5.0], 0.8) == False
    check(has_close_elements)

def test_hidden_suite_case_005():

    def check(has_close_elements):
        assert has_close_elements([1.0, 2.0, 3.0, 4.0, 5.0, 2.0], 0.1) == True
    check(has_close_elements)

def test_hidden_suite_case_006():

    def check(has_close_elements):
        assert has_close_elements([1.1, 2.2, 3.1, 4.1, 5.1], 1.0) == True
    check(has_close_elements)

def test_hidden_suite_case_007():

    def check(has_close_elements):
        assert has_close_elements([1.1, 2.2, 3.1, 4.1, 5.1], 0.5) == False
    check(has_close_elements)
