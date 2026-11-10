"""Find the Duplicate Number at n = 10^5: one value repeated once or many times, the rest
distinct values from 1..n."""

SEEDS = 3
N = 10**5


def generate(rng):
    dup = rng.randint(1, N)
    copies = rng.choice([2, 3, N // 2])
    others = rng.sample([v for v in range(1, N + 1) if v != dup], N + 1 - copies)
    nums = others + [dup] * copies
    rng.shuffle(nums)
    return {"nums": nums}
