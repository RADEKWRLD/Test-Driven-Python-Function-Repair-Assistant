import pytest

from solution import split_escaped


def test_empty_text_is_one_empty_field():
    assert split_escaped("") == [""]


def test_plain_split_preserves_leading_middle_and_trailing_empty_fields():
    assert split_escaped(",a,,b,") == ["", "a", "", "b", ""]


def test_escape_quotes_a_delimiter():
    assert split_escaped("north\\,west,south") == ["north,west", "south"]


def test_two_escapes_do_not_quote_the_following_delimiter():
    text = "left" + "\\" * 2 + ",right"
    assert split_escaped(text) == ["left\\", "right"]


def test_four_escapes_decode_to_two_literal_escapes():
    assert split_escaped("\\" * 4) == ["\\" * 2]


def test_unmatched_trailing_escape_is_literal():
    assert split_escaped("end\\") == ["end\\"]


def test_custom_delimiter_and_escape():
    assert split_escaped("a!|b|c", delimiter="|", escape="!") == ["a|b", "c"]


def test_invalid_delimiter_and_escape_are_rejected():
    for delimiter, escape in [("", "\\"), (",", ""), ("::", "\\"), ("!", "!")]:
        with pytest.raises(ValueError):
            split_escaped("", delimiter, escape)
