"""Maximum Average Subarray I at n = 10^5 with k from 1 to n, where re-summing every window is
quadratic for mid-sized k."""

SEEDS = 3
N = 10**5


def generate(rng):
    nums = [rng.randint(-(10**4), 10**4) for _ in range(N)]
    k = rng.choice([N // 2, rng.randint(1, N), N])
    return {"nums": nums, "k": k}
