import pytest

from solution import erase_marked


def test_empty_input():
    assert erase_marked("") == ""


def test_unescaped_markers_delete_previous_characters():
    assert erase_marked("abc##d") == "ad"


def test_markers_on_empty_output_do_nothing():
    assert erase_marked("###a#") == ""


def test_escaped_marker_is_literal():
    assert erase_marked("a\\#b") == "a#b"


def test_marker_after_escaped_escape_is_active():
    assert erase_marked("a" + "\\" * 2 + "#") == "a"


def test_escape_pairs_are_consumed_once():
    assert erase_marked("\\" * 4) == "\\" * 2


def test_unmatched_trailing_escape_is_literal():
    assert erase_marked("x\\") == "x\\"


def test_invalid_marker_and_escape_are_rejected():
    for marker, escape in [("", "\\"), ("##", "\\"), ("#", ""), ("!", "!")]:
        with pytest.raises(ValueError):
            erase_marked("", marker, escape)
