"""The Number of Full Rounds You Have Played: login and logout times as hh:mm."""


def _valid(t: str) -> bool:
    return (
        isinstance(t, str)
        and len(t) == 5
        and t[2] == ":"
        and t[:2].isdigit()
        and t[3:].isdigit()
        and int(t[:2]) <= 23
        and int(t[3:]) <= 59
    )


def check(loginTime: str, logoutTime: str) -> None:
    assert _valid(loginTime), "loginTime is hh:mm with 00 <= hh <= 23, 00 <= mm <= 59"
    assert _valid(logoutTime), "logoutTime is hh:mm with 00 <= hh <= 23, 00 <= mm <= 59"
    assert loginTime != logoutTime, "loginTime and logoutTime are not equal"
