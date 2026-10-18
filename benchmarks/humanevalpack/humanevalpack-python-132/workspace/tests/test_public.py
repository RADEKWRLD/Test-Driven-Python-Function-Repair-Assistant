from solution import *  # noqa: F403


def test_public_examples():
    def check(is_nested):
        # Check some simple cases
        assert is_nested('[[]]') == True, "This prints if this assert fails 1 (good for debugging!)"
        assert is_nested('[]]]]]]][[[[[]') == False
        assert is_nested('[][]') == False
        assert is_nested('[]') == False
        assert is_nested('[[]][[') == True
        assert is_nested('[[][]]') == True
        # Check some edge cases that are easy to work out by hand.
    check(is_nested)
