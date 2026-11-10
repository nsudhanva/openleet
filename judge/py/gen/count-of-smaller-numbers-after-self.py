"""Count of Smaller Numbers After Self at n = 10^5: descending order (every pair is an
inversion), or random values in [-10^4, 10^4] with many duplicates."""

SEEDS = 2
N = 10**5


def generate(rng):
    nums = [rng.randint(-(10**4), 10**4) for _ in range(N)]
    if rng.random() < 0.5:
        nums.sort(reverse=True)
    return {"nums": nums}
