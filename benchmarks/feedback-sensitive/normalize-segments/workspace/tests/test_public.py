from solution import normalize_segments


def test_empty_relative_path():
    assert normalize_segments("") == "."


def test_repeated_slashes_and_dot_segments():
    assert normalize_segments("a//./b/") == "a/b"


def test_relative_parent_cancels_normal_segment():
    assert normalize_segments("a/b/../c") == "a/c"


def test_absolute_parent_does_not_go_above_root():
    assert normalize_segments("/../../a/../") == "/"


def test_repeated_leading_parents_are_preserved():
    assert normalize_segments("../../a") == "../../a"


def test_parent_after_canceled_segment_preserves_unresolved_parent():
    assert normalize_segments("../a/../../b") == "../../b"


def test_absolute_spelling_and_trailing_slash():
    assert normalize_segments("///x//y/") == "/x/y"


def test_backslash_is_an_ordinary_character():
    assert normalize_segments("a\\b/./c") == "a\\b/c"
