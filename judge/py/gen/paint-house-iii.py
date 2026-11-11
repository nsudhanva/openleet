"""Paint House III with the maximum 100 houses and 20 colors, a tenth of them painted from a
hidden coloring with exactly `target` = 10 neighborhoods, so searching colorings without
memoization explodes where the O(m * n^2 * target) DP does ~4 * 10^5 steps."""

SEEDS = 2
M = 100
N = 20
TARGET = 10


def generate(rng):
    cuts = sorted(rng.sample(range(1, M), TARGET - 1))
    hidden, color = [], 0
    for size in (b - a for a, b in zip([0, *cuts], [*cuts, M], strict=True)):
        color = rng.choice([c for c in range(1, N + 1) if c != color])
        hidden += [color] * size
    houses = [c if rng.random() < 0.1 else 0 for c in hidden]
    cost = [[rng.randint(1, 10**4) for _ in range(N)] for _ in range(M)]
    return {"houses": houses, "cost": cost, "m": M, "n": N, "target": TARGET}
