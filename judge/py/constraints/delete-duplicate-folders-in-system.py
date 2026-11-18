"""Delete Duplicate Folders in System: absolute folder paths, each a list of folder names."""


def check(paths: list[list[str]]) -> None:
    assert 1 <= len(paths) <= 2 * 10**4, "1 <= paths.length <= 2 * 10^4"
    assert all(1 <= len(p) <= 500 for p in paths), "1 <= paths[i].length <= 500"
    assert all(isinstance(x, str) for p in paths for x in p), "paths[i][j] is a string"
    assert all(1 <= len(x) <= 10 for p in paths for x in p), "1 <= paths[i][j].length <= 10"
    total = sum(len(x) for p in paths for x in p)
    assert 1 <= total <= 2 * 10**5, "1 <= sum(paths[i][j].length) <= 2 * 10^5"
    assert all("a" <= c <= "z" for p in paths for x in p for c in x), (
        "path[i][j] consists of lowercase English letters"
    )
    seen = {tuple(p) for p in paths}
    assert len(seen) == len(paths), "no two paths lead to the same folder"
    assert all(tuple(p[:-1]) in seen for p in paths if len(p) > 1), (
        "for any folder not at the root level, its parent folder is also in the input"
    )
