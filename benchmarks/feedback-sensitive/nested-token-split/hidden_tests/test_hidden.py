import pytest

from solution import split_top_level


def test_deep_nesting_with_inner_empty_fields():
    assert split_top_level("p,(((,)),q),r") == ["p", "(((,)),q)", "r"]


def test_neighboring_nested_groups():
    assert split_top_level("((a),b),((c),d)") == ["((a),b)", "((c),d)"]


def test_empty_parentheses_inside_outer_pair():
    assert split_top_level("((),x),") == ["((),x)", ""]


def test_unicode_delimiter_obeys_depth():
    assert split_top_level("甲、(乙、(丙)、丁)、戊", "、") == ["甲", "(乙、(丙)、丁)", "戊"]


def test_quotes_do_not_protect_delimiters():
    assert split_top_level('"x,y",z') == ['"x', 'y"', "z"]


def test_backslash_does_not_escape_delimiter():
    assert split_top_level("a\\,b") == ["a\\", "b"]


def test_whitespace_and_nonseparator_characters_preserved():
    assert split_top_level("  left , (right) , end ") == ["  left ", " (right) ", " end "]


def test_nested_text_with_no_top_level_delimiter():
    assert split_top_level("((m,n),o)") == ["((m,n),o)"]


def test_balanced_total_count_does_not_allow_wrong_order():
    with pytest.raises(ValueError):
        split_top_level("x),y,(z")
    with pytest.raises(ValueError):
        split_top_level("((u),v")


def test_custom_delimiter_empty_fields_and_validation():
    assert split_top_level("|((a)|b)||", "|") == ["", "((a)|b)", "", ""]
    with pytest.raises(ValueError):
        split_top_level("value", "||")
