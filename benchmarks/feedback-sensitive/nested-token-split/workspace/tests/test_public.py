import pytest

from solution import split_top_level


def test_empty_text_is_one_empty_field():
    assert split_top_level("") == [""]


def test_top_level_empty_fields_are_preserved():
    assert split_top_level(",a,,b,") == ["", "a", "", "b", ""]


def test_single_parenthesis_level_protects_delimiters():
    assert split_top_level("a,(b,c),d") == ["a", "(b,c)", "d"]


def test_inner_close_does_not_end_outer_protection():
    assert split_top_level("a,(b,(c,d),e),f") == ["a", "(b,(c,d),e)", "f"]


def test_multiple_nested_closures_keep_outer_depth():
    assert split_top_level("((x),y),z") == ["((x),y)", "z"]


def test_custom_delimiter():
    assert split_top_level("a;(b;c);d", ";") == ["a", "(b;c)", "d"]


def test_invalid_delimiter_is_rejected():
    for delimiter in ("", "::", "(", ")"):
        with pytest.raises(ValueError):
            split_top_level("", delimiter)


def test_unmatched_parentheses_are_rejected():
    for text in ("a,(b", "a),b", ")("):
        with pytest.raises(ValueError):
            split_top_level(text)
