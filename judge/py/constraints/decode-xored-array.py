"""Decode XORed Array: the XOR-encoded array and the first element."""


def check(encoded: list[int], first: int) -> None:
    n = len(encoded) + 1
    assert 2 <= n <= 10**4, "2 <= n <= 10^4"
    assert all(0 <= v <= 10**5 for v in encoded), "0 <= encoded[i] <= 10^5"
    assert 0 <= first <= 10**5, "0 <= first <= 10^5"
