"""Find Substring With Given Hash Value: a lowercase string and polynomial hash parameters."""


def check(s: str, power: int, modulo: int, k: int, hashValue: int) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= k <= len(s) <= 2 * 10**4, "1 <= k <= s.length <= 2 * 10^4"
    assert 1 <= power <= 10**9 and 1 <= modulo <= 10**9, "1 <= power, modulo <= 10^9"
    assert 0 <= hashValue < modulo, "0 <= hashValue < modulo"
    assert all("a" <= c <= "z" for c in s), "s consists of lowercase English letters only"
    n = len(s)
    val = [ord(c) - 96 for c in s]
    top = pow(power, k - 1, modulo)
    h = 0
    for j in range(k):
        h = (h + val[n - k + j] * pow(power, j, modulo)) % modulo
    found = h == hashValue
    for i in range(n - k - 1, -1, -1):
        h = ((h - val[i + k] * top) * power + val[i]) % modulo
        found = found or h == hashValue
    assert found, "an answer always exists"
