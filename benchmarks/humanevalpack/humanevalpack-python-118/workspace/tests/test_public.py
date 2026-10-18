from solution import *  # noqa: F403


def test_public_examples():
    def check(get_closest_vowel):
        # Check some simple cases
        assert get_closest_vowel("yogurt") == "u"
        assert get_closest_vowel("FULL") == "U"
        assert get_closest_vowel("ab") == ""
        assert get_closest_vowel("quick") == ""
    check(get_closest_vowel)
