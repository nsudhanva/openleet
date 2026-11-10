"""Sum of Subsequence Widths at n = 10^5, where only the sort-and-powers formula is fast and
the modulo must be applied carefully."""

SEEDS = 2
N = 10**5


def generate(rng):
    if rng.random() < 0.5:
        nums = [rng.randint(1, 10**5) for _ in range(N)]
    else:
        nums = [rng.choice([1, 10**5, rng.randint(1, 10**5)]) for _ in range(N)]
    return {"nums": nums}
