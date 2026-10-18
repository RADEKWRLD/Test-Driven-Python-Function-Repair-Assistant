from solution import *  # noqa: F403


def test_public_examples():
    def check(words_in_sentence):
        # Check some simple cases
        assert words_in_sentence("This is a test") == "is"
        assert words_in_sentence("lets go for swimming") == "go for"
    check(words_in_sentence)
