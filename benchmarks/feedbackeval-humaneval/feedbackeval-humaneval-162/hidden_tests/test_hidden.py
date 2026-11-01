from solution import *

def test_hidden_suite_case_001():

    def check(string_to_md5):
        assert string_to_md5('Hello world') == '3e25960a79dbc69b674cd4ec67a72c62'
    check(string_to_md5)

def test_hidden_suite_case_002():

    def check(string_to_md5):
        assert string_to_md5('') == None
    check(string_to_md5)

def test_hidden_suite_case_003():

    def check(string_to_md5):
        assert string_to_md5('A B C') == '0ef78513b0cb8cef12743f5aeb35f888'
    check(string_to_md5)

def test_hidden_suite_case_004():

    def check(string_to_md5):
        assert string_to_md5('password') == '5f4dcc3b5aa765d61d8327deb882cf99'
    check(string_to_md5)

def test_hidden_suite_case_005():

    def check(string_to_md5):
        assert True
    check(string_to_md5)
