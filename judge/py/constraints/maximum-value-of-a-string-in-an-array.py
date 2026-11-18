"""Maximum Value of a String in an Array: strings of lowercase letters and digits."""

import string


def check(strs: list[str]) -> None:
    assert 1 <= len(strs) <= 100, "1 <= strs.length <= 100"
    assert all(1 <= len(s) <= 9 for s in strs), "1 <= strs[i].length <= 9"
    allowed = set(string.ascii_lowercase + string.digits)
    assert all(set(s) <= allowed for s in strs), (
        "strs[i] consists of only lowercase English letters and digits"
    )
