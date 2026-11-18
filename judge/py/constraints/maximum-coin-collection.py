"""Maximum Coin Collection: coin values on two lanes."""


def check(lane1: list[int], lane2: list[int]) -> None:
    assert 1 <= len(lane1) <= 10**5, "1 <= lane1.length <= 10^5"
    assert len(lane1) == len(lane2), "lane1.length == lane2.length"
    assert all(-(10**9) <= v <= 10**9 for v in lane1), "-10^9 <= lane1[i] <= 10^9"
    assert all(-(10**9) <= v <= 10**9 for v in lane2), "-10^9 <= lane2[i] <= 10^9"
