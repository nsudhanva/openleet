"""Most Stones Removed with Same Row or Column: distinct [x, y] stone coordinates."""


def check(stones: list[list[int]]) -> None:
    assert 1 <= len(stones) <= 1000, "1 <= stones.length <= 1000"
    assert all(len(s) == 2 for s in stones), "stones[i].length == 2"
    assert all(0 <= v <= 10**4 for s in stones for v in s), "0 <= xi, yi <= 10^4"
    assert len({(x, y) for x, y in stones}) == len(stones), (
        "no two stones are at the same coordinate point"
    )
