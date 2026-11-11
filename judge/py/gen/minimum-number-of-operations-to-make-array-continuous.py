"""Minimum Number of Operations to Make Array Continuous at n = 2 * 10^4: values spread over
about 3n with some repeats, so counting the values in each candidate window by a full scan is
~4 * 10^8 steps."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    base = rng.randint(1, 10**9 - 3 * N)
    nums = [base + rng.randrange(3 * N) for _ in range(N)]
    return {"nums": nums}
