import pytest

from solution import tokenize_quoted


def test_empty_and_unquoted_whitespace():
    assert tokenize_quoted("") == []
    assert tokenize_quoted(" \t\n ") == []


def test_unquoted_words_split_on_whitespace():
    assert tokenize_quoted(" alpha\tbeta\ngamma ") == ["alpha", "beta", "gamma"]


def test_quoted_whitespace_is_preserved():
    assert tokenize_quoted('one "two three" four') == ["one", "two three", "four"]


def test_adjacent_quoted_and_unquoted_fragments_concatenate():
    assert tokenize_quoted('pre"mid dle"post') == ["premid dlepost"]


def test_empty_quoted_token_is_not_dropped():
    assert tokenize_quoted('""') == [""]


def test_empty_tokens_between_words_are_retained():
    assert tokenize_quoted('a "" b ""') == ["a", "", "b", ""]


def test_backslash_is_literal():
    assert tokenize_quoted("a\\b c") == ["a\\b", "c"]


def test_unmatched_quote_is_rejected():
    with pytest.raises(ValueError):
        tokenize_quoted('left "right')
