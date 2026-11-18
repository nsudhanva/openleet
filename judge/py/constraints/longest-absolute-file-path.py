"""Longest Absolute File Path: a file system written as lines indented by tabs."""


def check(input: str) -> None:
    assert isinstance(input, str), "input is a string"
    assert 1 <= len(input) <= 10**4, "1 <= input.length <= 10^4"
    assert all(c.isascii() and (c.isalnum() or c in "\n\t. ") for c in input), (
        "input has only letters, digits, '\\n', '\\t', '.' and ' '"
    )
    prev_depth = -1
    prev_is_file = False
    for line in input.split("\n"):
        name = line.lstrip("\t")
        depth = len(line) - len(name)
        assert "\t" not in name, "tabs only appear as indentation"
        assert len(name) > 0, "all file and directory names have positive length"
        assert depth <= prev_depth + 1, "the file system is valid (indentation)"
        assert not (prev_is_file and depth > prev_depth), "a file has no children"
        dots = name.count(".")
        assert dots <= 1, "a file name is of the form name.extension"
        prev_depth, prev_is_file = depth, bool(dots)
