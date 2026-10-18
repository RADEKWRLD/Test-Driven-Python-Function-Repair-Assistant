from solution import *  # noqa: F403


def test_public_examples():
    def check(triples_sum_to_zero):
        assert triples_sum_to_zero([1, 3, 5, 0]) == False
        assert triples_sum_to_zero([1, 3, -2, 1]) == True
        assert triples_sum_to_zero([1, 2, 3, 7]) == False
        assert triples_sum_to_zero([2, 4, -5, 3, 9, 7]) == True
    check(triples_sum_to_zero)
