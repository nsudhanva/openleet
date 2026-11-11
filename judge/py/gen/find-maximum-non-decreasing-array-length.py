"""Find Maximum Non-decreasing Array Length at n = 10^5: a first element near 10^5 followed by
small values, so for tens of thousands of indices the last valid split point lies far back and a
quadratic DP scans ~10^9 candidates."""

SEEDS = 2
N = 10**5


def generate(rng):
    top = rng.choice([2, 3])
    nums = [rng.randint(9 * 10**4, 10**5)] + [rng.randint(1, top) for _ in range(N - 1)]
    return {"nums": nums}
