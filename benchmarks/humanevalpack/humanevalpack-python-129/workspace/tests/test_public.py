from solution import *

def test_public_examples_case_001():

    def check(minPath):
        assert minPath([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 3) == [1, 2, 1]
    check(minPath)

def test_public_examples_case_002():

    def check(minPath):
        assert minPath([[5, 9, 3], [4, 1, 6], [7, 8, 2]], 1) == [1]
    check(minPath)
