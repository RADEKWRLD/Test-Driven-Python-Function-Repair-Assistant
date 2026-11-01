import pytest

from solution import split_escaped


def test_odd_escape_run_keeps_delimiter_inside_field():
    assert split_escaped("p" + "\\" * 3 + ",q") == ["p\\,q"]


def test_six_escapes_release_the_following_delimiter():
    assert split_escaped("\\" * 6 + ",tail") == ["\\" * 3, "tail"]


def test_multiple_independent_escape_runs():
    text = "a" + "\\" * 2 + ",b\\,c," + "\\" * 4 + ","
    assert split_escaped(text) == ["a\\", "b,c", "\\" * 2, ""]


def test_ordinary_character_can_be_quoted():
    assert split_escaped("ab\\xcd,e") == ["abxcd", "e"]


def test_trailing_odd_escape_run_preserves_unmatched_escape():
    assert split_escaped("z" + "\\" * 5) == ["z" + "\\" * 3]


def test_only_delimiters_preserve_every_empty_field():
    assert split_escaped(",,,") == ["", "", "", ""]


def test_custom_escape_is_itself_quotable():
    assert split_escaped("x!!;y!;z", delimiter=";", escape="!") == ["x!", "y;z"]


def test_unicode_delimiter_and_escape():
    assert split_escaped("甲※※、乙※、丙", delimiter="、", escape="※") == ["甲※", "乙、丙"]


def test_invalid_parameters_rejected_for_nonempty_text():
    for delimiter, escape in [("xx", "!"), (";", "!!"), ("q", "q"), ("", "")]:
        with pytest.raises(ValueError):
            split_escaped("payload", delimiter, escape)


def test_long_escape_runs_follow_pair_consumption():
    for count in range(7, 21):
        text = "v" + "\\" * count + ",w"
        prefix = "v" + "\\" * (count // 2)
        expected = [prefix + ",w"] if count % 2 else [prefix, "w"]
        assert split_escaped(text) == expected, (count, text)
