from solution import *

def test_hidden_suite_case_001():

    def check(digitSum):
        assert True, 'This prints if this assert fails 1 (good for debugging!)'
    check(digitSum)

def test_hidden_suite_case_002():

    def check(digitSum):
        assert digitSum('') == 0, 'Error'
    check(digitSum)

def test_hidden_suite_case_003():

    def check(digitSum):
        assert digitSum('abAB') == 131, 'Error'
    check(digitSum)

def test_hidden_suite_case_004():

    def check(digitSum):
        assert digitSum('abcCd') == 67, 'Error'
    check(digitSum)

def test_hidden_suite_case_005():

    def check(digitSum):
        assert digitSum('helloE') == 69, 'Error'
    check(digitSum)

def test_hidden_suite_case_006():

    def check(digitSum):
        assert digitSum('woArBld') == 131, 'Error'
    check(digitSum)

def test_hidden_suite_case_007():

    def check(digitSum):
        assert digitSum('aAaaaXa') == 153, 'Error'
    check(digitSum)

def test_hidden_suite_case_008():

    def check(digitSum):
        assert True, 'This prints if this assert fails 2 (also good for debugging!)'
    check(digitSum)

def test_hidden_suite_case_009():

    def check(digitSum):
        assert digitSum(' How are yOu?') == 151, 'Error'
    check(digitSum)

def test_hidden_suite_case_010():

    def check(digitSum):
        assert digitSum('You arE Very Smart') == 327, 'Error'
    check(digitSum)
