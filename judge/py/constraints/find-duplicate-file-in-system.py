"""Find Duplicate File in System: directory info strings "dir f1.txt(content) f2.txt(content)"."""

import re

_CHARS = re.compile(r"[A-Za-z0-9/.() ]*")


def check(paths: list[str]) -> None:
    assert 1 <= len(paths) <= 2 * 10**4, "1 <= paths.length <= 2 * 10^4"
    assert all(isinstance(p, str) for p in paths), "paths[i] is a string"
    assert all(1 <= len(p) <= 3000 for p in paths), "1 <= paths[i].length <= 3000"
    assert 1 <= sum(len(p) for p in paths) <= 5 * 10**5, "1 <= sum(paths[i].length) <= 5 * 10^5"
    assert all(_CHARS.fullmatch(p) for p in paths), (
        "paths[i] consists of letters, digits, '/', '.', '(', ')', ' '"
    )
    dirs = [p.split(" ")[0] for p in paths]
    assert len(set(dirs)) == len(dirs), "each directory info represents a unique directory"
    for p in paths:
        parts = p.split(" ")
        assert len(parts) >= 2, "a single blank space separates the directory path and file info"
        names = []
        for f in parts[1:]:
            assert "(" in f and f.endswith(")"), "files are written name(content)"
            names.append(f[: f.index("(")])
        assert len(set(names)) == len(names), "no files share the same name in the same directory"
