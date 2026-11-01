from solution import normalize_segments


def test_root_and_root_dot():
    assert normalize_segments("/") == "/"
    assert normalize_segments("/./") == "/"


def test_relative_path_that_cancels_to_empty():
    assert normalize_segments("x/../y/..") == "."


def test_three_unresolved_parents_stay_distinct():
    assert normalize_segments("../../../") == "../../.."


def test_dot_between_unresolved_parents_does_not_change_them():
    assert normalize_segments(".././../leaf/..") == "../.."


def test_long_chain_preserves_every_unresolved_parent():
    assert normalize_segments("one/../../two/../../three") == "../../three"


def test_normal_segment_after_parents_can_be_canceled():
    assert normalize_segments("../../folder/../item") == "../../item"


def test_unicode_and_spaces_are_ordinary_segment_content():
    assert normalize_segments("/甲/ /../乙/...") == "/甲/乙/..."


def test_backslashes_are_not_path_separators():
    assert normalize_segments("..\\..//x/..") == "..\\.."


def test_absolute_many_parents_clamp_to_root():
    assert normalize_segments("/a/b/../../../../c//") == "/c"


def test_many_leading_parents_with_balanced_normal_suffix():
    for count in range(4, 13):
        parents = "/".join([".."] * count)
        assert normalize_segments(parents + "/node/child/../..") == parents, count
