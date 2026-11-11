"""Maximum Product of First and Last Elements of a Subsequence with 2 * 10^4 random values and a
small m, so trying every pair of ends is quadratic."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    nums = [rng.randint(-(10**5), 10**5) for _ in range(N)]
    return {"nums": nums, "m": rng.randint(1, 50)}
