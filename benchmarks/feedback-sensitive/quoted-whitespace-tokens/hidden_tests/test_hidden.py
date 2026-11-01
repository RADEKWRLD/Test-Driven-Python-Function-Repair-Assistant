import pytest

from solution import tokenize_quoted


def test_separated_empty_quoted_tokens():
    assert tokenize_quoted('""\t""\n""') == ["", "", ""]


def test_adjacent_empty_fragments_are_one_token():
    assert tokenize_quoted('""""') == [""]


def test_empty_fragments_around_word_do_not_create_extra_tokens():
    assert tokenize_quoted('""word"" ""end') == ["word", "end"]


def test_only_quoted_spaces_are_a_real_token():
    assert tokenize_quoted('"  \t "') == ["  \t "]


def test_unicode_whitespace_splits_only_outside_quotes():
    assert tokenize_quoted('甲\u2003"乙\u2003丙"\u00a0""') == ["甲", "乙\u2003丙", ""]


def test_backslash_does_not_escape_a_quote():
    assert tokenize_quoted('x\\"y z"') == ["x\\y z"]


def test_single_quotes_are_ordinary_characters():
    assert tokenize_quoted("'left right'") == ["'left", "right'"]


def test_whitespace_around_empty_token_is_ignored():
    assert tokenize_quoted(' \r\n""\t ') == [""]


def test_many_concatenated_fragments_and_internal_newline():
    assert tokenize_quoted('a"b"c"d\ne"f') == ["abcd\nef"]


def test_unmatched_quote_after_complete_tokens_raises():
    with pytest.raises(ValueError):
        tokenize_quoted('"" done "')
    with pytest.raises(ValueError):
        tokenize_quoted('\\"')
