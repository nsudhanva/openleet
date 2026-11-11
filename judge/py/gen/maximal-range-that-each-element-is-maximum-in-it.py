"""Maximal Range That Each Element Is Maximum in It at n = 3 * 10^4 distinct values: a mountain
(rising then falling) with light noise, so expanding from every element is ~2 * 10^8 steps."""

SEEDS = 2
N = 3 * 10**4
TOP = 10**5


def generate(rng):
    vals = sorted(rng.sample(range(1, TOP + 1), N))
    peak = rng.randrange(N // 4, 3 * N // 4)
    up = sorted(rng.sample(vals[:-1], peak))
    taken = set(up)
    down = sorted((v for v in vals[:-1] if v not in taken), reverse=True)
    nums = [*up, vals[-1], *down]
    # A few nearby swaps break exact monotonicity without shortening the ranges much.
    for _ in range(N // 100):
        i = rng.randrange(N - 1)
        nums[i], nums[i + 1] = nums[i + 1], nums[i]
    return {"nums": nums}
