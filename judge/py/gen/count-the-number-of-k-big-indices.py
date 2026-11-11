"""Count the Number of K-Big Indices at n = 10^5 with k = n / 10, so counting smaller values on
both sides of every index costs 10^10 steps."""

SEEDS = 2
N = 10**5


def generate(rng):
    return {"nums": [rng.randint(1, N) for _ in range(N)], "k": N // 10}
