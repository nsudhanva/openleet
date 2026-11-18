"""High-Access Employees: [name, "HHMM"] access records."""

LETTERS = set("abcdefghijklmnopqrstuvwxyz")
DIGITS = set("0123456789")


def check(access_times: list[list[str]]) -> None:
    assert 1 <= len(access_times) <= 100, "1 <= access_times.length <= 100"
    assert all(len(r) == 2 for r in access_times), "access_times[i].length == 2"
    for name, t in (r for r in access_times):
        assert 1 <= len(name) <= 10, "1 <= access_times[i][0].length <= 10"
        assert set(name) <= LETTERS, "access_times[i][0] consists only of English small letters"
        assert len(t) == 4, "access_times[i][1].length == 4"
        assert set(t) <= DIGITS, "access_times[i][1] consists only of '0' to '9'"
        assert int(t[:2]) <= 23 and int(t[2:]) <= 59, "access_times[i][1] is in 24-hour time format"
