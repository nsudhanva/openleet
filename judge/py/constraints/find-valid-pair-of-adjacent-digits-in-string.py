"""Find Valid Pair of Adjacent Digits in String: a string of digits 1 to 9."""


def check(s: str) -> None:
    assert 2 <= len(s) <= 100, "2 <= s.length <= 100"
    assert all("1" <= c <= "9" for c in s), "s only consists of digits from '1' to '9'"
