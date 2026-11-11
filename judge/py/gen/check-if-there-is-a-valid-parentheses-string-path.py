"""Check if There Is a Valid Parentheses String Path on a 21 x 20 grid: every path reads
()()...((() (and a few ')' turned '(' only raise the balance), which stays feasible until the
last cell and ends unbalanced, so exploring the paths without memoization is exponential."""

SEEDS = 2
M, N = 21, 20


def generate(rng):
    m, n = (M, N) if rng.random() < 0.5 else (N, M)
    path = "()" * ((m + n - 1) // 2 - 2) + "((()"
    grid = [[path[i + j] for j in range(n)] for i in range(m)]
    for _ in range(m * n // 100):
        i, j = rng.randrange(m), rng.randrange(n)
        if 0 < i + j < m + n - 6:
            grid[i][j] = "("
    return {"grid": grid}
