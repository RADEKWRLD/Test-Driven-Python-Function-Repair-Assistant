from solution import *

def test_public_examples_case_001():

    def check(valid_date):
        assert valid_date('03-11-2000') == True
    check(valid_date)

def test_public_examples_case_002():

    def check(valid_date):
        assert valid_date('15-01-2012') == False
    check(valid_date)

def test_public_examples_case_003():

    def check(valid_date):
        assert valid_date('04-0-2040') == False
    check(valid_date)

def test_public_examples_case_004():

    def check(valid_date):
        assert valid_date('06-04-2020') == True
    check(valid_date)

def test_public_examples_case_005():

    def check(valid_date):
        assert valid_date('06/04/2020') == False
    check(valid_date)
