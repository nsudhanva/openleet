"""Find All Groups of Farmland: an m x n binary grid whose groups of 1s are separate rectangles."""


def check(land: list[list[int]]) -> None:
    m = len(land)
    assert 1 <= m <= 300, "1 <= m <= 300"
    n = len(land[0])
    assert 1 <= n <= 300, "1 <= n <= 300"
    assert all(len(row) == n for row in land), "n == land[i].length"
    assert all(v in (0, 1) for row in land for v in row), "land consists of only 0's and 1's"
    seen = [[False] * n for _ in range(m)]
    for r in range(m):
        for c in range(n):
            if land[r][c] != 1 or seen[r][c]:
                continue
            seen[r][c] = True
            stack = [(r, c)]
            count = 0
            r1 = r2 = r
            c1 = c2 = c
            while stack:
                y, x = stack.pop()
                count += 1
                r1, r2 = min(r1, y), max(r2, y)
                c1, c2 = min(c1, x), max(c2, x)
                for ny, nx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
                    if 0 <= ny < m and 0 <= nx < n and land[ny][nx] == 1 and not seen[ny][nx]:
                        seen[ny][nx] = True
                        stack.append((ny, nx))
            assert count == (r2 - r1 + 1) * (c2 - c1 + 1), (
                "groups of farmland are rectangular in shape"
            )
