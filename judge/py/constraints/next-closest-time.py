"""Next Closest Time: a valid time string "HH:MM"."""


def check(time: str) -> None:
    assert len(time) == 5, "time.length == 5"
    assert time[2] == ":" and time[:2].isdigit() and time[3:].isdigit(), (
        'time is in the form "HH:MM"'
    )
    assert time[:2].isascii() and time[3:].isascii(), 'time is in the form "HH:MM"'
    assert 0 <= int(time[:2]) < 24, "0 <= HH < 24"
    assert 0 <= int(time[3:]) < 60, "0 <= MM < 60"
