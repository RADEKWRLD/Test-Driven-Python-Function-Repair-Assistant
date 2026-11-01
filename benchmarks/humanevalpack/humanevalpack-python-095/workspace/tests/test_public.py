from solution import *

def test_public_examples_case_001():

    def check(check_dict_case):
        assert check_dict_case({'p': 'pineapple', 'b': 'banana'}) == True, 'First test error: ' + str(check_dict_case({'p': 'pineapple', 'b': 'banana'}))
    check(check_dict_case)

def test_public_examples_case_002():

    def check(check_dict_case):
        assert check_dict_case({'p': 'pineapple', 'A': 'banana', 'B': 'banana'}) == False, 'Second test error: ' + str(check_dict_case({'p': 'pineapple', 'A': 'banana', 'B': 'banana'}))
    check(check_dict_case)

def test_public_examples_case_003():

    def check(check_dict_case):
        assert check_dict_case({'p': 'pineapple', 8: 'banana', 'a': 'apple'}) == False, 'Third test error: ' + str(check_dict_case({'p': 'pineapple', 5: 'banana', 'a': 'apple'}))
    check(check_dict_case)

def test_public_examples_case_004():

    def check(check_dict_case):
        assert check_dict_case({'Name': 'John', 'Age': '36', 'City': 'Houston'}) == False, 'Fourth test error: ' + str(check_dict_case({'Name': 'John', 'Age': '36', 'City': 'Houston'}))
    check(check_dict_case)

def test_public_examples_case_005():

    def check(check_dict_case):
        assert check_dict_case({'STATE': 'NC', 'ZIP': '12345'}) == True, 'Fifth test error: ' + str(check_dict_case({'STATE': 'NC', 'ZIP': '12345'}))
    check(check_dict_case)
