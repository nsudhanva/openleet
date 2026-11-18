"""Maximum Area of a Piece of Cake After Cuts: cake size and two lists of cut positions."""


def check(h: int, w: int, horizontalCuts: list[int], verticalCuts: list[int]) -> None:
    assert 2 <= h <= 10**9 and 2 <= w <= 10**9, "2 <= h, w <= 10^9"
    assert 1 <= len(horizontalCuts) <= min(h - 1, 10**5), (
        "1 <= horizontalCuts.length <= min(h - 1, 10^5)"
    )
    assert 1 <= len(verticalCuts) <= min(w - 1, 10**5), (
        "1 <= verticalCuts.length <= min(w - 1, 10^5)"
    )
    assert all(1 <= c < h for c in horizontalCuts), "1 <= horizontalCuts[i] < h"
    assert all(1 <= c < w for c in verticalCuts), "1 <= verticalCuts[i] < w"
    assert len(set(horizontalCuts)) == len(horizontalCuts), "horizontalCuts are distinct"
    assert len(set(verticalCuts)) == len(verticalCuts), "verticalCuts are distinct"
