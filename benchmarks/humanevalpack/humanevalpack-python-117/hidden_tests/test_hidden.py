from solution import *

def test_hidden_suite_case_001():

    def check(select_words):
        assert select_words('Mary had a little lamb', 4) == ['little'], 'First test error: ' + str(select_words('Mary had a little lamb', 4))
    check(select_words)

def test_hidden_suite_case_002():

    def check(select_words):
        assert select_words('Mary had a little lamb', 3) == ['Mary', 'lamb'], 'Second test error: ' + str(select_words('Mary had a little lamb', 3))
    check(select_words)

def test_hidden_suite_case_003():

    def check(select_words):
        assert select_words('simple white space', 2) == [], 'Third test error: ' + str(select_words('simple white space', 2))
    check(select_words)

def test_hidden_suite_case_004():

    def check(select_words):
        assert select_words('Hello world', 4) == ['world'], 'Fourth test error: ' + str(select_words('Hello world', 4))
    check(select_words)

def test_hidden_suite_case_005():

    def check(select_words):
        assert select_words('Uncle sam', 3) == ['Uncle'], 'Fifth test error: ' + str(select_words('Uncle sam', 3))
    check(select_words)

def test_hidden_suite_case_006():

    def check(select_words):
        assert select_words('', 4) == [], '1st edge test error: ' + str(select_words('', 4))
    check(select_words)

def test_hidden_suite_case_007():

    def check(select_words):
        assert select_words('a b c d e f', 1) == ['b', 'c', 'd', 'f'], '2nd edge test error: ' + str(select_words('a b c d e f', 1))
    check(select_words)
