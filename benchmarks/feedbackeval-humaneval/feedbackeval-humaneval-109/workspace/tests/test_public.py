from solution import *

def test_public_examples_case_001():

    def check(move_one_ball):
        assert move_one_ball([3, 4, 5, 1, 2]) == True, 'This prints if this assert fails 1 (good for debugging!)'
    check(move_one_ball)

def test_public_examples_case_002():

    def check(move_one_ball):
        assert move_one_ball([3, 5, 4, 1, 2]) == False, 'This prints if this assert fails 2 (also good for debugging!)'
    check(move_one_ball)
