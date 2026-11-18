"""Grid Teleportation Traversal: a grid of '#', '.' and uppercase letters."""


def check(matrix: list[str]) -> None:
    m = len(matrix)
    assert 1 <= m <= 10**3, "1 <= m <= 10^3"
    assert all(isinstance(r, str) for r in matrix), "matrix is an array of strings"
    n = len(matrix[0])
    assert all(len(r) == n for r in matrix), "n == matrix[i].length"
    assert 1 <= n <= 10**3, "1 <= n <= 10^3"
    assert all(c in "#." or "A" <= c <= "Z" for r in matrix for c in r), (
        "matrix[i][j] is either '#', '.', or an uppercase English letter"
    )
    assert matrix[0][0] != "#", "matrix[0][0] is not an obstacle"
