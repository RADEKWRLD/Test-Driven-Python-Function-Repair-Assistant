from solution import *  # noqa: F403


def test_public_examples():
    def check(string_to_md5):
        # Check some simple cases
        assert string_to_md5('Hello world') == '3e25960a79dbc69b674cd4ec67a72c62'
        # Check some edge cases that are easy to work out by hand.
        assert True
    check(string_to_md5)
