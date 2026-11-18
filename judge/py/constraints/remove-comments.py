"""Remove Comments: lines of a C++ program with line and block comments."""


def check(source: list[str]) -> None:
    assert 1 <= len(source) <= 100, "1 <= source.length <= 100"
    assert all(0 <= len(line) <= 80 for line in source), "0 <= source[i].length <= 80"
    assert all(32 <= ord(c) <= 126 for line in source for c in line), (
        "source[i] consists of printable ASCII characters"
    )
    assert not any(c in "'\"" for line in source for c in line), (
        "there are no single-quote or double-quote in the input"
    )
    in_block = False
    for line in source:
        i = 0
        while i < len(line):
            if in_block:
                end = line.find("*/", i)
                if end < 0:
                    break
                in_block, i = False, end + 2
            elif line.startswith("//", i):
                break
            elif line.startswith("/*", i):
                in_block, i = True, i + 2
            else:
                i += 1
    assert not in_block, "every open block comment is eventually closed"
