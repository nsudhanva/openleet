"""Alert Using Same Key-Card Three or More Times in a One Hour Period: names and times."""

import re


def check(keyName: list[str], keyTime: list[str]) -> None:
    assert 1 <= len(keyName) <= 10**5, "1 <= keyName.length <= 10^5"
    assert 1 <= len(keyTime) <= 10**5, "1 <= keyTime.length <= 10^5"
    assert len(keyName) == len(keyTime), "keyName.length == keyTime.length"
    assert all(isinstance(t, str) and re.fullmatch(r"[0-9]{2}:[0-9]{2}", t) for t in keyTime), (
        'keyTime[i] is in the format "HH:MM"'
    )
    assert all(int(t[:2]) <= 23 and int(t[3:]) <= 59 for t in keyTime), (
        "keyTime[i] is a valid 24-hour time"
    )
    assert len(set(zip(keyName, keyTime, strict=True))) == len(keyName), (
        "[keyName[i], keyTime[i]] is unique"
    )
    assert all(1 <= len(s) <= 10 for s in keyName), "1 <= keyName[i].length <= 10"
    assert all(s.isascii() and s.isalpha() and s.islower() for s in keyName), (
        "keyName[i] contains only lowercase English letters"
    )
