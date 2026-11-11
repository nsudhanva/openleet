"""Count the Number of Square-Free Subsets at n = 1000 values in 1..30, so listing the
astronomically many square-free subsets is hopeless while the prime-mask DP has 1024 states."""

SEEDS = 2
N = 1000
LIMIT = 30


def generate(rng):
    return {"nums": [rng.randint(1, LIMIT) for _ in range(N)]}
