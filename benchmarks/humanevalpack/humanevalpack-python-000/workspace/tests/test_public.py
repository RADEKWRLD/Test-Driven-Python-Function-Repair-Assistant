from solution import *

def test_public_examples_case_001():

    def check(has_close_elements):
        assert has_close_elements([1.0, 2.0, 3.0], 0.5) == False
    check(has_close_elements)

def test_public_examples_case_002():

    def check(has_close_elements):
        assert has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3) == True
    check(has_close_elements)
