"""Maximum Area Rectangle With Point Constraints II: x and y coordinates of unique points."""


def check(xCoord: list[int], yCoord: list[int]) -> None:
    assert 1 <= len(xCoord) <= 2 * 10**5, "1 <= xCoord.length <= 2 * 10^5"
    assert len(xCoord) == len(yCoord), "xCoord.length == yCoord.length"
    assert all(0 <= v <= 8 * 10**7 for v in xCoord), "0 <= xCoord[i] <= 8 * 10^7"
    assert all(0 <= v <= 8 * 10**7 for v in yCoord), "0 <= yCoord[i] <= 8 * 10^7"
    assert len(set(zip(xCoord, yCoord, strict=True))) == len(xCoord), "all points are unique"
