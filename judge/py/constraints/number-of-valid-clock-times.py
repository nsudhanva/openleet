"""Number of Valid Clock Times: an "hh:mm" string with some digits replaced by '?'."""


def check(time: str) -> None:
    assert isinstance(time, str), "time is a string"
    assert len(time) == 5, "time has length 5"
    assert time[2] == ":", "format is hh:mm"
    digits = time[:2] + time[3:]
    assert all(c == "?" or c in "0123456789" for c in digits), "digits or '?'"
    hours = [f"{h:02d}" for h in range(24)]
    minutes = [f"{m:02d}" for m in range(60)]

    def fits(pat: str, options: list[str]) -> bool:
        return any(all(p == "?" or p == c for p, c in zip(pat, o, strict=True)) for o in options)

    assert fits(time[:2], hours), '"00" <= hh <= "23"'
    assert fits(time[3:], minutes), '"00" <= mm <= "59"'
