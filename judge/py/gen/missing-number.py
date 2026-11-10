"""Missing Number at n = 10^4: a shuffled 0..n with one value removed (sometimes 0 or n)."""

SEEDS = 3
N = 10**4


def generate(rng):
    missing = rng.choice((0, N, rng.randint(0, N)))
    nums = [v for v in range(N + 1) if v != missing]
    rng.shuffle(nums)
    return {"nums": nums}
