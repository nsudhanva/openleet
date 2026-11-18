"""Greatest Common Divisor of Strings: two uppercase strings."""


def check(str1: str, str2: str) -> None:
    for name, s in (("str1", str1), ("str2", str2)):
        assert 1 <= len(s) <= 1000, f"1 <= {name}.length <= 1000"
        assert all("A" <= c <= "Z" for c in s), f"{name} consists of English uppercase letters"
