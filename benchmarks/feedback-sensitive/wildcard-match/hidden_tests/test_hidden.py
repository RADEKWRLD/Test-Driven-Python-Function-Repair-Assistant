from itertools import product

from solution import wildcard_match


def test_only_star_matches_a_long_text():
    assert wildcard_match("abcdefghijk", "*") is True


def test_leading_star_consumes_prefix():
    assert wildcard_match("some-prefix-tail", "*tail") is True


def test_trailing_star_consumes_suffix():
    assert wildcard_match("head-and-some-more", "head*") is True


def test_consecutive_stars_still_match_arbitrary_length():
    assert wildcard_match("abcdefg", "a**g") is True


def test_unicode_characters_match_question_and_star():
    assert wildcard_match("甲乙丙丁戊", "?*戊") is True
    assert wildcard_match("🙂", "?") is True


def test_star_includes_newline_and_whitespace():
    assert wildcard_match("a\n \tb", "a*b") is True


def test_literal_suffix_still_required_after_star():
    assert wildcard_match("abcdef", "a*z") is False
    assert wildcard_match("abcdef", "*de") is False


def test_backslash_is_literal_and_does_not_escape_star():
    assert wildcard_match("\\long", "\\*") is True
    assert wildcard_match("long", "\\*") is False


def test_questions_require_enough_characters_between_stars():
    assert wildcard_match("x", "*??*") is False
    assert wildcard_match("xy", "*??*") is True


def test_bounded_cases_match_independent_recursive_expansion():
    def expected(text, pattern):
        if not pattern:
            return not text
        if pattern[0] == "*":
            return any(expected(text[count:], pattern[1:]) for count in range(len(text) + 1))
        return bool(text) and (pattern[0] == "?" or pattern[0] == text[0]) and expected(text[1:], pattern[1:])

    for text_length in range(1, 4):
        for letters in product("xy", repeat=text_length):
            text = "".join(letters)
            for pattern_length in range(1, 4):
                for tokens in product("xy?*", repeat=pattern_length):
                    pattern = "".join(tokens)
                    assert wildcard_match(text, pattern) is expected(text, pattern), (text, pattern)
    for length in range(2, 11):
        assert wildcard_match("a" + "x" * length + "b" + "y" * length + "c", "a*b*c") is True
    assert wildcard_match("aabc", "a*c?") is False
