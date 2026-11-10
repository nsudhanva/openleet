"""Kth Smallest in a Sorted Matrix at n = 300 (9 * 10^4 cells) built so rows and columns are
non-decreasing, with wide values or many duplicates."""

SEEDS = 2
N = 300


def generate(rng):
    step = rng.choice([2, 3 * 10**6])
    start = -(10**9)
    m = [[0] * N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            base = start
            if i:
                base = max(base, m[i - 1][j])
            if j:
                base = max(base, m[i][j - 1])
            m[i][j] = base + rng.randint(0, step)
    return {"matrix": m, "k": rng.randint(1, N * N)}
