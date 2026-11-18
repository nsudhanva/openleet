"""Find The Original Array of Prefix Xor: an array of prefix xor values."""


def check(pref: list[int]) -> None:
    assert 1 <= len(pref) <= 10**5, "1 <= pref.length <= 10^5"
    assert all(0 <= v <= 10**6 for v in pref), "0 <= pref[i] <= 10^6"
