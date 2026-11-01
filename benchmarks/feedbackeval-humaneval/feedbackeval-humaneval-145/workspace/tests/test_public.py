from solution import *

def test_public_examples_case_001():

    def check(order_by_points):
        assert order_by_points([1, 11, -1, -11, -12]) == [-1, -11, 1, -12, 11]
    check(order_by_points)

def test_public_examples_case_002():

    def check(order_by_points):
        assert order_by_points([]) == []
    check(order_by_points)
