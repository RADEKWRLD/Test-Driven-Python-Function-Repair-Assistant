from solution import *

def test_public_examples_case_001():

    def check(is_happy):
        assert is_happy('a') == False, 'a'
    check(is_happy)

def test_public_examples_case_002():

    def check(is_happy):
        assert is_happy('aa') == False, 'aa'
    check(is_happy)

def test_public_examples_case_003():

    def check(is_happy):
        assert is_happy('abcd') == True, 'abcd'
    check(is_happy)

def test_public_examples_case_004():

    def check(is_happy):
        assert is_happy('aabb') == False, 'aabb'
    check(is_happy)

def test_public_examples_case_005():

    def check(is_happy):
        assert is_happy('adb') == True, 'adb'
    check(is_happy)

def test_public_examples_case_006():

    def check(is_happy):
        assert is_happy('xyy') == False, 'xyy'
    check(is_happy)
