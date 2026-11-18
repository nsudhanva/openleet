"""Crawler Log Folder: change-folder operations "../", "./" or "name/"."""

import string


def check(logs: list[str]) -> None:
    assert 1 <= len(logs) <= 10**3, "1 <= logs.length <= 10^3"
    allowed = set(string.ascii_lowercase + string.digits)
    for s in logs:
        assert isinstance(s, str), "logs[i] is a string"
        assert 2 <= len(s) <= 10, "2 <= logs[i].length <= 10"
        assert s.endswith("/"), "logs[i] follows the format: ends with '/'"
        name = s[:-1]
        assert name in (".", "..") or (name != "" and set(name) <= allowed), (
            "logs[i] is '../', './' or a folder name of lowercase letters and digits"
        )
