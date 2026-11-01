from solution import *

def test_public_examples_case_001():

    def check(find_closest_elements):
        assert find_closest_elements([1.0, 2.0, 3.0, 4.0, 5.0, 2.2]) == (2.0, 2.2)
    check(find_closest_elements)

def test_public_examples_case_002():

    def check(find_closest_elements):
        assert find_closest_elements([1.0, 2.0, 3.0, 4.0, 5.0, 2.0]) == (2.0, 2.0)
    check(find_closest_elements)
