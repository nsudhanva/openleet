"""Hash Divided String: a lowercase string whose length is divisible by k."""


def check(s: str, k: int) -> None:
    assert 1 <= k <= 100, "1 <= k <= 100"
    assert k <= len(s) <= 1000, "k <= s.length <= 1000"
    assert len(s) % k == 0, "s.length is divisible by k"
    assert all("a" <= c <= "z" for c in s), "s consists only of lowercase English letters"
