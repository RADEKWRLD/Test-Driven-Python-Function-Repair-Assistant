from solution import *

def test_hidden_suite_case_001():

    def check(encode):
        assert encode('TEST') == 'tgst', 'This prints if this assert fails 1 (good for debugging!)'
    check(encode)

def test_hidden_suite_case_002():

    def check(encode):
        assert encode('Mudasir') == 'mWDCSKR', 'This prints if this assert fails 2 (good for debugging!)'
    check(encode)

def test_hidden_suite_case_003():

    def check(encode):
        assert encode('YES') == 'ygs', 'This prints if this assert fails 3 (good for debugging!)'
    check(encode)

def test_hidden_suite_case_004():

    def check(encode):
        assert encode('This is a message') == 'tHKS KS C MGSSCGG', 'This prints if this assert fails 2 (also good for debugging!)'
    check(encode)

def test_hidden_suite_case_005():

    def check(encode):
        assert encode('I DoNt KnOw WhAt tO WrItE') == 'k dQnT kNqW wHcT Tq wRkTg', 'This prints if this assert fails 2 (also good for debugging!)'
    check(encode)
