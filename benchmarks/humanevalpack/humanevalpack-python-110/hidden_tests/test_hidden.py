from solution import *

def test_hidden_suite_case_001():

    def check(exchange):
        assert exchange([1, 2, 3, 4], [1, 2, 3, 4]) == 'YES'
    check(exchange)

def test_hidden_suite_case_002():

    def check(exchange):
        assert exchange([1, 2, 3, 4], [1, 5, 3, 4]) == 'NO'
    check(exchange)

def test_hidden_suite_case_003():

    def check(exchange):
        assert exchange([1, 2, 3, 4], [2, 1, 4, 3]) == 'YES'
    check(exchange)

def test_hidden_suite_case_004():

    def check(exchange):
        assert exchange([5, 7, 3], [2, 6, 4]) == 'YES'
    check(exchange)

def test_hidden_suite_case_005():

    def check(exchange):
        assert exchange([5, 7, 3], [2, 6, 3]) == 'NO'
    check(exchange)

def test_hidden_suite_case_006():

    def check(exchange):
        assert exchange([3, 2, 6, 1, 8, 9], [3, 5, 5, 1, 1, 1]) == 'NO'
    check(exchange)

def test_hidden_suite_case_007():

    def check(exchange):
        assert exchange([100, 200], [200, 200]) == 'YES'
    check(exchange)
