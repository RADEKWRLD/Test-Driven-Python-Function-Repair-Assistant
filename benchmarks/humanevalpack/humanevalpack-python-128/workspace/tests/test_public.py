from solution import *  # noqa: F403


def test_public_examples():
    def check(prod_signs):
        # Check some simple cases
        assert True, "This prints if this assert fails 1 (good for debugging!)"
        assert prod_signs([1, 2, 2, -4]) == -9
        assert prod_signs([0, 1]) == 0
        assert prod_signs([]) == None
    check(prod_signs)
