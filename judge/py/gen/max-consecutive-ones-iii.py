"""Max Consecutive Ones III at n = 10^5 with varied k (0, small, or huge), where trying every
start is quadratic."""

SEEDS = 3
N = 10**5


def generate(rng):
    p = rng.choice([0.5, 0.9, 0.1])
    nums = [1 if rng.random() < p else 0 for _ in range(N)]
    k = rng.choice([0, rng.randint(1, 100), rng.randint(0, N)])
    return {"nums": nums, "k": k}
