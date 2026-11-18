"""Remove Methods From Project: n methods, a suspicious method k and invocation pairs."""


def check(n: int, k: int, invocations: list[list[int]]) -> None:
    assert isinstance(n, int) and isinstance(k, int), "n and k are integers"
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert 0 <= k <= n - 1, "0 <= k <= n - 1"
    assert 0 <= len(invocations) <= 2 * 10**5, "0 <= invocations.length <= 2 * 10^5"
    assert all(len(p) == 2 for p in invocations), "invocations[i] == [ai, bi]"
    assert all(0 <= a <= n - 1 and 0 <= b <= n - 1 for a, b in invocations), "0 <= ai, bi <= n - 1"
    assert all(a != b for a, b in invocations), "ai != bi"
    assert len({tuple(p) for p in invocations}) == len(invocations), (
        "invocations[i] != invocations[j]"
    )
