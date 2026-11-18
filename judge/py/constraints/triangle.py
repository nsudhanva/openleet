"""Triangle: a triangle of integers, row i holding i + 1 values."""


def check(triangle: list[list[int]]) -> None:
    assert 1 <= len(triangle) <= 200, "1 <= triangle.length <= 200"
    assert len(triangle[0]) == 1, "triangle[0].length == 1"
    assert all(len(triangle[i]) == len(triangle[i - 1]) + 1 for i in range(1, len(triangle))), (
        "triangle[i].length == triangle[i - 1].length + 1"
    )
    assert all(-(10**4) <= v <= 10**4 for r in triangle for v in r), (
        "-10^4 <= triangle[i][j] <= 10^4"
    )
