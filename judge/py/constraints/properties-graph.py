"""Properties Graph: an n x m matrix of small integers and a threshold k."""


def check(properties: list[list[int]], k: int) -> None:
    n = len(properties)
    assert 1 <= n <= 100, "1 <= n == properties.length <= 100"
    assert all(isinstance(r, list) for r in properties), "properties is a matrix"
    m = len(properties[0])
    assert 1 <= m <= 100, "1 <= m == properties[i].length <= 100"
    assert all(len(r) == m for r in properties), "m == properties[i].length"
    assert all(1 <= v <= 100 for r in properties for v in r), "1 <= properties[i][j] <= 100"
    assert 1 <= k <= m, "1 <= k <= m"
