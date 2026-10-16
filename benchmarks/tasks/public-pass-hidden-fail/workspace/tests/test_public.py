from solution import normalize_whitespace


def test_empty_string():
    assert normalize_whitespace("") == ""


def test_one_word():
    assert normalize_whitespace("hello") == "hello"


def test_single_spaces_are_preserved():
    assert normalize_whitespace("hello world") == "hello world"


def test_leading_space_is_removed():
    assert normalize_whitespace(" hello") == "hello"


def test_trailing_space_is_removed():
    assert normalize_whitespace("world ") == "world"
