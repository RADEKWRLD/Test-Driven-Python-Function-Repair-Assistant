from solution import *

def test_hidden_suite_case_001():

    def check(find_closest_elements):
        assert find_closest_elements([1.0, 2.0, 3.9, 4.0, 5.0, 2.2]) == (3.9, 4.0)
    check(find_closest_elements)

def test_hidden_suite_case_002():

    def check(find_closest_elements):
        assert find_closest_elements([1.0, 2.0, 5.9, 4.0, 5.0]) == (5.0, 5.9)
    check(find_closest_elements)

def test_hidden_suite_case_003():

    def check(find_closest_elements):
        assert find_closest_elements([1.0, 2.0, 3.0, 4.0, 5.0, 2.2]) == (2.0, 2.2)
    check(find_closest_elements)

def test_hidden_suite_case_004():

    def check(find_closest_elements):
        assert find_closest_elements([1.0, 2.0, 3.0, 4.0, 5.0, 2.0]) == (2.0, 2.0)
    check(find_closest_elements)

def test_hidden_suite_case_005():

    def check(find_closest_elements):
        assert find_closest_elements([1.1, 2.2, 3.1, 4.1, 5.1]) == (2.2, 3.1)
    check(find_closest_elements)
