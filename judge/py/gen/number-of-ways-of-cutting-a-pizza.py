"""Number of Ways of Cutting a Pizza at the maximum 50 by 50 with k = 10 and apples only along the
bottom row and right column, so nearly every cut is valid and trying each sequence of cuts without
a memo explores an exponential number of them."""

SEEDS = 2
N = 50
K = 10


def generate(rng):
    density = rng.uniform(0.3, 0.7)
    pizza = [["."] * N for _ in range(N)]
    for i in range(N):
        if rng.random() < density:
            pizza[i][N - 1] = "A"
        if rng.random() < density:
            pizza[N - 1][i] = "A"
    return {"pizza": ["".join(row) for row in pizza], "k": K}
