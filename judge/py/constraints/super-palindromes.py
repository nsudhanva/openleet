"""Super Palindromes: two decimal strings left <= right."""


def check(left: str, right: str) -> None:
    for name, s in (("left", left), ("right", right)):
        assert 1 <= len(s) <= 18, f"1 <= {name}.length <= 18"
        assert s.isascii() and s.isdigit(), f"{name} consists of only digits"
        assert s[0] != "0", f"{name} has no leading zeros"
        assert 1 <= int(s) <= 10**18 - 1, f"{name} in [1, 10^18 - 1]"
    assert int(left) <= int(right), "left <= right"
