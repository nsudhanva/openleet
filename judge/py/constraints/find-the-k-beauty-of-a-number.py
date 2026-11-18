"""Find the K-Beauty of a Number: an integer and a substring length k."""


def check(num: int, k: int) -> None:
    assert 1 <= num <= 10**9, "1 <= num <= 10^9"
    assert 1 <= k <= len(str(num)), "1 <= k <= num.length (taking num as a string)"
