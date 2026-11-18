"""Maximum Square Area by Removing Fences From a Field: field size m x n and distinct
horizontal and vertical fence positions."""


def check(m: int, n: int, hFences: list[int], vFences: list[int]) -> None:
    assert 3 <= m <= 10**9 and 3 <= n <= 10**9, "3 <= m, n <= 10^9"
    assert 1 <= len(hFences) <= 600, "1 <= hFences.length <= 600"
    assert 1 <= len(vFences) <= 600, "1 <= vFences.length <= 600"
    assert all(1 < h < m for h in hFences), "1 < hFences[i] < m"
    assert all(1 < v < n for v in vFences), "1 < vFences[i] < n"
    assert len(set(hFences)) == len(hFences), "hFences are unique"
    assert len(set(vFences)) == len(vFences), "vFences are unique"
