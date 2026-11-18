"""Remove Sub-Folders from the Filesystem: a list of unique absolute folder paths."""

import re

_PATH = re.compile(r"(?:/[a-z]+)+")


def check(folder: list[str]) -> None:
    assert isinstance(folder, list), "folder is a list"
    assert 1 <= len(folder) <= 4 * 10**4, "1 <= folder.length <= 4 * 10^4"
    assert all(isinstance(f, str) for f in folder), "folder[i] is a string"
    assert all(2 <= len(f) <= 100 for f in folder), "2 <= folder[i].length <= 100"
    assert all(f.startswith("/") for f in folder), "folder[i] always starts with '/'"
    assert all(_PATH.fullmatch(f) for f in folder), (
        "path is one or more of '/' followed by lowercase letters"
    )
    assert len(set(folder)) == len(folder), "each folder name is unique"
