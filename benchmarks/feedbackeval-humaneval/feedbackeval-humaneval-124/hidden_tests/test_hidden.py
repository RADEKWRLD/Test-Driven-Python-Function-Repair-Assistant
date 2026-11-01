from solution import *

def test_hidden_suite_case_001():

    def check(valid_date):
        assert valid_date('03-11-2000') == True
    check(valid_date)

def test_hidden_suite_case_002():

    def check(valid_date):
        assert valid_date('15-01-2012') == False
    check(valid_date)

def test_hidden_suite_case_003():

    def check(valid_date):
        assert valid_date('04-0-2040') == False
    check(valid_date)

def test_hidden_suite_case_004():

    def check(valid_date):
        assert valid_date('06-04-2020') == True
    check(valid_date)

def test_hidden_suite_case_005():

    def check(valid_date):
        assert valid_date('01-01-2007') == True
    check(valid_date)

def test_hidden_suite_case_006():

    def check(valid_date):
        assert valid_date('03-32-2011') == False
    check(valid_date)

def test_hidden_suite_case_007():

    def check(valid_date):
        assert valid_date('') == False
    check(valid_date)

def test_hidden_suite_case_008():

    def check(valid_date):
        assert valid_date('04-31-3000') == False
    check(valid_date)

def test_hidden_suite_case_009():

    def check(valid_date):
        assert valid_date('06-06-2005') == True
    check(valid_date)

def test_hidden_suite_case_010():

    def check(valid_date):
        assert valid_date('21-31-2000') == False
    check(valid_date)

def test_hidden_suite_case_011():

    def check(valid_date):
        assert valid_date('04-12-2003') == True
    check(valid_date)

def test_hidden_suite_case_012():

    def check(valid_date):
        assert valid_date('04122003') == False
    check(valid_date)

def test_hidden_suite_case_013():

    def check(valid_date):
        assert valid_date('20030412') == False
    check(valid_date)

def test_hidden_suite_case_014():

    def check(valid_date):
        assert valid_date('2003-04') == False
    check(valid_date)

def test_hidden_suite_case_015():

    def check(valid_date):
        assert valid_date('2003-04-12') == False
    check(valid_date)

def test_hidden_suite_case_016():

    def check(valid_date):
        assert valid_date('04-2003') == False
    check(valid_date)
