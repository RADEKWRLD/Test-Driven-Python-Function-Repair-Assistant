from solution import *

def test_hidden_suite_case_001():

    def check(solve):
        assert solve('AsDf') == 'aSdF'
    check(solve)

def test_hidden_suite_case_002():

    def check(solve):
        assert solve('1234') == '4321'
    check(solve)

def test_hidden_suite_case_003():

    def check(solve):
        assert solve('ab') == 'AB'
    check(solve)

def test_hidden_suite_case_004():

    def check(solve):
        assert solve('#a@C') == '#A@c'
    check(solve)

def test_hidden_suite_case_005():

    def check(solve):
        assert solve('#AsdfW^45') == '#aSDFw^45'
    check(solve)

def test_hidden_suite_case_006():

    def check(solve):
        assert solve('#6@2') == '2@6#'
    check(solve)

def test_hidden_suite_case_007():

    def check(solve):
        assert solve('#$a^D') == '#$A^d'
    check(solve)

def test_hidden_suite_case_008():

    def check(solve):
        assert solve('#ccc') == '#CCC'
    check(solve)
