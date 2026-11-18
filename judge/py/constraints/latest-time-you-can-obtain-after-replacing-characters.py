"""Latest Time You Can Obtain After Replacing Characters: an hh:mm string with '?' digits."""


def check(s: str) -> None:
    assert len(s) == 5, "s.length == 5"
    assert s[2] == ":", 's[2] is equal to ":"'
    assert all((c.isascii() and c.isdigit()) or c == "?" for i, c in enumerate(s) if i != 2), (
        'all characters except s[2] are digits or "?"'
    )
    assert any(
        all(p == "?" or p == c for p, c in zip(s, f"{h:02d}:{m:02d}", strict=False))
        for h in range(12)
        for m in range(60)
    ), "some time between 00:00 and 11:59 can be obtained"
