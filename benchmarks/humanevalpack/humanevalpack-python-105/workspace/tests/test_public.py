from solution import *  # noqa: F403


def test_public_examples():
    def check(by_length):
        # Check some simple cases
        assert True, "This prints if this assert fails 1 (good for debugging!)"
        assert by_length([2, 1, 1, 4, 5, 8, 2, 3]) == ["Eight", "Five", "Four", "Three", "Two", "Two", "One", "One"], "Error"
        assert by_length([]) == [], "Error"
        assert by_length([1, -1 , 55]) == ['One'], "Error"
        # Check some edge cases that are easy to work out by hand.
    check(by_length)
