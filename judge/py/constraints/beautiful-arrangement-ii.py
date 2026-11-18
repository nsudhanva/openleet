"""Beautiful Arrangement II: integers n and k."""


def check(n: int, k: int) -> None:
    assert isinstance(n, int) and isinstance(k, int), "n and k are integers"
    assert 1 <= k < n <= 10**4, "1 <= k < n <= 10^4"
