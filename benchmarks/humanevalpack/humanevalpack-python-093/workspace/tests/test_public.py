from solution import *  # noqa: F403


def test_public_examples():
    def check(encode):
        # Check some simple cases
        assert encode('test') == 'TGST', "This prints if this assert fails 1 (good for debugging!)"
        # Check some edge cases that are easy to work out by hand.
        assert encode('This is a message') == 'tHKS KS C MGSSCGG', "This prints if this assert fails 2 (also good for debugging!)"
    check(encode)
