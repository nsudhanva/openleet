"""Sum Game: an even-length string of digits and '?'."""


def check(num: str) -> None:
    assert 2 <= len(num) <= 10**5, "2 <= num.length <= 10^5"
    assert len(num) % 2 == 0, "num.length is even"
    assert all(c == "?" or "0" <= c <= "9" for c in num), "num consists of only digits and '?'"
