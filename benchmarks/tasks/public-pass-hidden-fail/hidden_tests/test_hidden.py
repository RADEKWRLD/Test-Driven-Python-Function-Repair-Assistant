from solution import normalize_whitespace


def test_repeated_spaces_collapse():
    assert normalize_whitespace("a   b") == "a b"


def test_tab_is_whitespace():
    assert normalize_whitespace("a\tb") == "a b"


def test_newline_is_whitespace():
    assert normalize_whitespace("a\nb") == "a b"


def test_mixed_whitespace_run():
    assert normalize_whitespace("  a \t\n b  ") == "a b"


def test_unicode_whitespace():
    assert normalize_whitespace("a\u2003b") == "a b"
