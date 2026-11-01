from solution import wildcard_match


def test_empty_pattern_and_text():
    assert wildcard_match("", "") is True
    assert wildcard_match("x", "") is False


def test_empty_text_requires_only_stars():
    assert wildcard_match("", "**") is True
    assert wildcard_match("", "?") is False


def test_literal_match_is_for_entire_string():
    assert wildcard_match("cat", "cat") is True
    assert wildcard_match("cats", "cat") is False


def test_question_matches_exactly_one_character():
    assert wildcard_match("cat", "c?t") is True
    assert wildcard_match("ct", "c?t") is False


def test_star_can_match_zero_or_one_character():
    assert wildcard_match("ab", "a*b") is True
    assert wildcard_match("acb", "a*b") is True


def test_star_can_consume_multiple_characters():
    assert wildcard_match("alphabet", "a*t") is True


def test_mixed_stars_and_questions():
    assert wildcard_match("prefix_middle_end", "pre*?end") is True


def test_regex_metacharacters_are_literals():
    assert wildcard_match("a.b[0]", "a.b[0]") is True
    assert wildcard_match("axb0", "a.b[0]") is False
