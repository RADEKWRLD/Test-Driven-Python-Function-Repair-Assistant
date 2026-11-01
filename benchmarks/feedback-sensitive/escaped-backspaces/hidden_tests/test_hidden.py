import pytest

from solution import erase_marked


def test_unescaped_marker_can_remove_a_quoted_marker():
    assert erase_marked("p\\##q") == "pq"


def test_three_escapes_quote_following_marker():
    assert erase_marked("u" + "\\" * 3 + "#v") == "u\\#v"


def test_six_escapes_then_marker_delete_one_literal_escape():
    assert erase_marked("\\" * 6 + "#") == "\\" * 2


def test_custom_marker_and_escape():
    assert erase_marked("ab!!*c", marker="*", escape="!") == "abc"


def test_ordinary_character_can_be_quoted_then_erased():
    assert erase_marked("12\\x##3") == "13"


def test_unicode_characters_are_erased_one_character_at_a_time():
    assert erase_marked("甲乙※※删丙", marker="删", escape="※") == "甲乙丙"


def test_trailing_odd_escape_run_preserves_unmatched_character():
    assert erase_marked("z" + "\\" * 5) == "z" + "\\" * 3


def test_markers_after_escaped_escape_can_empty_output():
    assert erase_marked("xy" + "\\" * 2 + "####z") == "z"


def test_invalid_parameters_with_nonempty_text():
    for marker, escape in [("*", "!!"), ("x", "x"), ("", "")]:
        with pytest.raises(ValueError):
            erase_marked("payload", marker, escape)


def test_long_escape_parity_controls_marker_interpretation():
    for count in range(7, 17):
        text = "a" + "\\" * count + "#"
        if count % 2:
            expected = "a" + "\\" * (count // 2) + "#"
        else:
            expected = "a" + "\\" * (count // 2 - 1)
        assert erase_marked(text) == expected, count
