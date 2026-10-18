from solution import *  # noqa: F403


def test_public_examples():
    def check(find_closest_elements):
        assert find_closest_elements([1.0, 2.0, 3.0, 4.0, 5.0, 2.2]) == (2.0, 2.2)
        assert find_closest_elements([1.0, 2.0, 3.0, 4.0, 5.0, 2.0]) == (2.0, 2.0)
    check(find_closest_elements)
