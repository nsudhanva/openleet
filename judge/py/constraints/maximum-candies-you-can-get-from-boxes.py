"""Maximum Candies You Can Get from Boxes: box status, candies, keys, contained boxes,
initial boxes."""


def check(
    status: list[int],
    candies: list[int],
    keys: list[list[int]],
    containedBoxes: list[list[int]],
    initialBoxes: list[int],
) -> None:
    n = len(status)
    assert n == len(candies) == len(keys) == len(containedBoxes), (
        "n == status.length == candies.length == keys.length == containedBoxes.length"
    )
    assert 1 <= n <= 1000, "1 <= n <= 1000"
    assert all(s in (0, 1) for s in status), "status[i] is either 0 or 1"
    assert all(1 <= c <= 1000 for c in candies), "1 <= candies[i] <= 1000"
    for ks in keys:
        assert 0 <= len(ks) <= n, "0 <= keys[i].length <= n"
        assert all(0 <= j < n for j in ks), "0 <= keys[i][j] < n"
        assert len(set(ks)) == len(ks), "all values of keys[i] are unique"
    seen = set()
    for cb in containedBoxes:
        assert 0 <= len(cb) <= n, "0 <= containedBoxes[i].length <= n"
        assert all(0 <= j < n for j in cb), "0 <= containedBoxes[i][j] < n"
        assert len(set(cb)) == len(cb), "all values of containedBoxes[i] are unique"
        assert not (seen & set(cb)), "each box is contained in one box at most"
        seen.update(cb)
    assert 0 <= len(initialBoxes) <= n, "0 <= initialBoxes.length <= n"
    assert all(0 <= j < n for j in initialBoxes), "0 <= initialBoxes[i] < n"
