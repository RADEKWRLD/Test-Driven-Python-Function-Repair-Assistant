from solution import *

def test_public_examples_case_001():

    def check(exchange):
        assert exchange([1, 2, 3, 4], [1, 2, 3, 4]) == 'YES'
    check(exchange)

def test_public_examples_case_002():

    def check(exchange):
        assert exchange([1, 2, 3, 4], [1, 5, 3, 4]) == 'NO'
    check(exchange)
