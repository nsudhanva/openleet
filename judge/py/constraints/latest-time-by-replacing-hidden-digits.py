"""Latest Time by Replacing Hidden Digits: an hh:mm time with '?' digits."""


def check(time: str) -> None:
    assert len(time) == 5 and time[2] == ":", "time is in the format hh:mm"
    digits = time[:2] + time[3:]
    assert all((c.isascii() and c.isdigit()) or c == "?" for c in digits), (
        "digits or '?' around ':'"
    )
    assert any(
        all(p == "?" or p == c for p, c in zip(time, f"{h:02d}:{m:02d}", strict=False))
        for h in range(24)
        for m in range(60)
    ), "a valid time can be produced"
