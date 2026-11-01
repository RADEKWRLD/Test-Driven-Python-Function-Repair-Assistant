from solution import *

def test_public_examples_case_001():

    def check(encode):
        assert encode('test') == 'TGST', 'This prints if this assert fails 1 (good for debugging!)'
    check(encode)

def test_public_examples_case_002():

    def check(encode):
        assert encode('This is a message') == 'tHKS KS C MGSSCGG', 'This prints if this assert fails 2 (also good for debugging!)'
    check(encode)
