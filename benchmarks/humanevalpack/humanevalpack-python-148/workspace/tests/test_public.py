from solution import *

def test_public_examples_case_001():

    def check(bf):
        assert bf('Jupiter', 'Neptune') == ('Saturn', 'Uranus'), 'First test error: ' + str(len(bf('Jupiter', 'Neptune')))
    check(bf)

def test_public_examples_case_002():

    def check(bf):
        assert bf('Earth', 'Mercury') == ('Venus',), 'Second test error: ' + str(bf('Earth', 'Mercury'))
    check(bf)

def test_public_examples_case_003():

    def check(bf):
        assert bf('Mercury', 'Uranus') == ('Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn'), 'Third test error: ' + str(bf('Mercury', 'Uranus'))
    check(bf)
