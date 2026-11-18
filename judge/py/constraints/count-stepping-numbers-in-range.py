"""Count Stepping Numbers in Range: two decimal strings low <= high."""


def _num(s: str) -> bool:
    return all("0" <= c <= "9" for c in s) and (s == "0" or s[0] != "0")


def check(low: str, high: str) -> None:
    assert isinstance(low, str) and isinstance(high, str), "strings"
    assert 1 <= len(low) <= 100, "1 <= low.length <= 100"
    assert 1 <= len(high) <= 100, "1 <= high.length <= 100"
    assert low.isdigit() and high.isdigit() and low.isascii() and high.isascii(), (
        "low and high consist of only digits"
    )
    assert _num(low) and _num(high), "low and high don't have any leading zeros"
    assert 1 <= int(low) <= int(high) < 10**100, "1 <= int(low) <= int(high) < 10^100"
