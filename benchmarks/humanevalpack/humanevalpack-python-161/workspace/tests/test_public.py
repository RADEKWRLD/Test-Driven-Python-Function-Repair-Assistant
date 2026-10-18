from solution import *  # noqa: F403


def test_public_examples():
    def check(solve):
        # Check some simple cases
        assert solve("1234") == "4321"
        assert solve("ab") == "AB"
        assert solve("#a@C") == "#A@c"
        # Don't remove this line:
    check(solve)
