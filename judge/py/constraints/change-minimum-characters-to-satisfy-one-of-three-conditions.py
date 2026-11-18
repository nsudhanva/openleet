"""Change Minimum Characters to Satisfy One of Three Conditions: two lowercase strings."""


def check(a: str, b: str) -> None:
    assert isinstance(a, str) and isinstance(b, str), "a, b are strings"
    assert 1 <= len(a) <= 10**5, "1 <= a.length <= 10^5"
    assert 1 <= len(b) <= 10**5, "1 <= b.length <= 10^5"
    assert all("a" <= c <= "z" for c in a + b), "a and b consist only of lowercase letters"
