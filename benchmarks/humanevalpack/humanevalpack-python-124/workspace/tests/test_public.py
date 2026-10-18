from solution import *  # noqa: F403


def test_public_examples():
    def check(valid_date):
        # Check some simple cases
        assert valid_date('03-11-2000') == True
        assert valid_date('15-01-2012') == False
        assert valid_date('04-0-2040') == False
        assert valid_date('06-04-2020') == True
        assert valid_date('06/04/2020') == False
    check(valid_date)
