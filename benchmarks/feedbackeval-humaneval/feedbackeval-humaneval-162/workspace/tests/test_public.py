from solution import *

def test_public_examples_case_001():

    def check(string_to_md5):
        assert string_to_md5('Hello world') == '3e25960a79dbc69b674cd4ec67a72c62'
    check(string_to_md5)

def test_public_examples_case_002():

    def check(string_to_md5):
        assert True
    check(string_to_md5)
