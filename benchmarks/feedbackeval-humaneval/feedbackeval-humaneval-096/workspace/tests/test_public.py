from solution import *

def test_public_examples_case_001():

    def check(count_up_to):
        assert count_up_to(5) == [2, 3]
    check(count_up_to)

def test_public_examples_case_002():

    def check(count_up_to):
        assert count_up_to(11) == [2, 3, 5, 7]
    check(count_up_to)

def test_public_examples_case_003():

    def check(count_up_to):
        assert count_up_to(0) == []
    check(count_up_to)

def test_public_examples_case_004():

    def check(count_up_to):
        assert count_up_to(20) == [2, 3, 5, 7, 11, 13, 17, 19]
    check(count_up_to)

def test_public_examples_case_005():

    def check(count_up_to):
        assert count_up_to(1) == []
    check(count_up_to)

def test_public_examples_case_006():

    def check(count_up_to):
        assert count_up_to(18) == [2, 3, 5, 7, 11, 13, 17]
    check(count_up_to)
