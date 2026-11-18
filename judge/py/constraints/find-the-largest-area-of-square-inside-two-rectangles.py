"""Find the Largest Area of Square Inside Two Rectangles: rectangle corners."""


def check(bottomLeft: list[list[int]], topRight: list[list[int]]) -> None:
    n = len(bottomLeft)
    assert n == len(topRight), "n == bottomLeft.length == topRight.length"
    assert 2 <= n <= 10**3, "2 <= n <= 10^3"
    assert all(len(p) == 2 for p in bottomLeft), "bottomLeft[i].length == 2"
    assert all(len(p) == 2 for p in topRight), "topRight[i].length == 2"
    assert all(1 <= v <= 10**7 for p in bottomLeft for v in p), "1 <= bottomLeft[i][j] <= 10^7"
    assert all(1 <= v <= 10**7 for p in topRight for v in p), "1 <= topRight[i][j] <= 10^7"
    assert all(bottomLeft[i][0] < topRight[i][0] for i in range(n)), (
        "bottomLeft[i][0] < topRight[i][0]"
    )
    assert all(bottomLeft[i][1] < topRight[i][1] for i in range(n)), (
        "bottomLeft[i][1] < topRight[i][1]"
    )
