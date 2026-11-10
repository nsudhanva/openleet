"""Longest Subarray With At Most K Frequency at n = 10^5, with few distinct values so the
window shrinks often, or all-distinct values so the answer is the whole array."""

SEEDS = 3
N = 10**5


def generate(rng):
    shape = rng.choice(["few", "distinct", "mid"])
    if shape == "distinct":
        nums = rng.sample(range(1, 10**9 + 1), N)
        k = rng.randint(1, 5)
    elif shape == "few":
        pool = [rng.randint(1, 10**9) for _ in range(rng.randint(2, 20))]
        nums = [rng.choice(pool) for _ in range(N)]
        k = rng.randint(1, 1000)
    else:
        nums = [rng.randint(1, 1000) for _ in range(N)]
        k = rng.randint(1, 200)
    return {"nums": nums, "k": k}
