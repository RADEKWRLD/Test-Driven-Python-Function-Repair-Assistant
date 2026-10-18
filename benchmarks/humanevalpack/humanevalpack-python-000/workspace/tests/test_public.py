from solution import *  # noqa: F403


def test_public_examples():
    def check(has_close_elements):
        assert has_close_elements([1.0, 2.0, 3.0], 0.5) == False
        assert has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3) == True
    check(has_close_elements)
