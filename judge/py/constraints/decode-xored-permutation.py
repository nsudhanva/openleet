"""Decode XORed Permutation: the XORs of adjacent elements of a permutation of 1..n, n odd."""


def check(encoded: list[int]) -> None:
    n = len(encoded) + 1
    assert 3 <= n < 10**5, "3 <= n < 10^5"
    assert n % 2 == 1, "n is odd"
    total = 0
    for v in range(1, n + 1):
        total ^= v
    odd = 0
    for i in range(1, n - 1, 2):
        odd ^= encoded[i]
    perm = [total ^ odd]
    for e in encoded:
        perm.append(perm[-1] ^ e)
    assert sorted(perm) == list(range(1, n + 1)), (
        "encoded comes from a permutation of the first n positive integers"
    )
