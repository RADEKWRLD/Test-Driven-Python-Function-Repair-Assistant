from solution import *

def test_hidden_suite_case_001():

    def check(bf):
        assert bf('Jupiter', 'Neptune') == ('Saturn', 'Uranus'), 'First test error: ' + str(len(bf('Jupiter', 'Neptune')))
    check(bf)

def test_hidden_suite_case_002():

    def check(bf):
        assert bf('Earth', 'Mercury') == ('Venus',), 'Second test error: ' + str(bf('Earth', 'Mercury'))
    check(bf)

def test_hidden_suite_case_003():

    def check(bf):
        assert bf('Mercury', 'Uranus') == ('Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn'), 'Third test error: ' + str(bf('Mercury', 'Uranus'))
    check(bf)

def test_hidden_suite_case_004():

    def check(bf):
        assert bf('Neptune', 'Venus') == ('Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus'), 'Fourth test error: ' + str(bf('Neptune', 'Venus'))
    check(bf)

def test_hidden_suite_case_005():

    def check(bf):
        assert bf('Earth', 'Earth') == ()
    check(bf)

def test_hidden_suite_case_006():

    def check(bf):
        assert bf('Mars', 'Earth') == ()
    check(bf)

def test_hidden_suite_case_007():

    def check(bf):
        assert bf('Jupiter', 'Makemake') == ()
    check(bf)
