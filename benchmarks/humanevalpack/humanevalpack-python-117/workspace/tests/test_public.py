from solution import *

def test_public_examples_case_001():

    def check(select_words):
        assert select_words('Mary had a little lamb', 4) == ['little'], 'First test error: ' + str(select_words('Mary had a little lamb', 4))
    check(select_words)

def test_public_examples_case_002():

    def check(select_words):
        assert select_words('Mary had a little lamb', 3) == ['Mary', 'lamb'], 'Second test error: ' + str(select_words('Mary had a little lamb', 3))
    check(select_words)

def test_public_examples_case_003():

    def check(select_words):
        assert select_words('simple white space', 2) == [], 'Third test error: ' + str(select_words('simple white space', 2))
    check(select_words)

def test_public_examples_case_004():

    def check(select_words):
        assert select_words('Hello world', 4) == ['world'], 'Fourth test error: ' + str(select_words('Hello world', 4))
    check(select_words)

def test_public_examples_case_005():

    def check(select_words):
        assert select_words('Uncle sam', 3) == ['Uncle'], 'Fifth test error: ' + str(select_words('Uncle sam', 3))
    check(select_words)
