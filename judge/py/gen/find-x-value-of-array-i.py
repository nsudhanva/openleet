"""X-Value of Array I at n = 10^5 with values up to 10^9 and k from 1 to 5, including runs of
multiples of k."""

SEEDS = 3
N = 10**5


def generate(rng):
    k = rng.choice([5, 4, rng.randint(1, 5)])
    if rng.random() < 0.5:
        nums = [rng.randint(1, 10**9) for _ in range(N)]
    else:
        nums = [
            rng.randint(1, 10**9 // k) * k if rng.random() < 0.01 else rng.randint(1, 10**9)
            for _ in range(N)
        ]
    return {"nums": nums, "k": k}
