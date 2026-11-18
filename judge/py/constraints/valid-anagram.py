"""Valid Anagram: two lowercase strings."""


def check(s: str, t: str) -> None:
    for name, x in (("s", s), ("t", t)):
        assert isinstance(x, str), f"{name} is a string"
        assert 1 <= len(x) <= 5 * 10**4, f"1 <= {name}.length <= 5 * 10^4"
        assert all("a" <= c <= "z" for c in x), f"{name} consists of lowercase English letters"
