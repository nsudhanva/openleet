"""Maximum Consecutive Floors Without Special Floors: bottom, top and unique special floors."""


def check(bottom: int, top: int, special: list[int]) -> None:
    assert 1 <= len(special) <= 10**5, "1 <= special.length <= 10^5"
    assert all(1 <= bottom <= v <= top <= 10**9 for v in special), (
        "1 <= bottom <= special[i] <= top <= 10^9"
    )
    assert len(set(special)) == len(special), "all values of special are unique"
