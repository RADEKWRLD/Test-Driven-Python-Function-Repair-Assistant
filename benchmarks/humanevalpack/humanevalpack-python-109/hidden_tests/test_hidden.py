from solution import *

def test_hidden_suite_case_001():

    def check(move_one_ball):
        assert move_one_ball([3, 4, 5, 1, 2]) == True, 'This prints if this assert fails 1 (good for debugging!)'
    check(move_one_ball)

def test_hidden_suite_case_002():

    def check(move_one_ball):
        assert move_one_ball([3, 5, 10, 1, 2]) == True
    check(move_one_ball)

def test_hidden_suite_case_003():

    def check(move_one_ball):
        assert move_one_ball([4, 3, 1, 2]) == False
    check(move_one_ball)

def test_hidden_suite_case_004():

    def check(move_one_ball):
        assert move_one_ball([3, 5, 4, 1, 2]) == False, 'This prints if this assert fails 2 (also good for debugging!)'
    check(move_one_ball)

def test_hidden_suite_case_005():

    def check(move_one_ball):
        assert move_one_ball([]) == True
    check(move_one_ball)
