"""Maximum of Minimum Values in All Subarrays with 2 * 10^4 values whose first three quarters
ascend, so taking the minimum of every subarray, or expanding from every element, is quadratic."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    a = sorted(rng.randint(0, 10**9) for _ in range(3 * N // 4))
    return {"nums": a + [rng.randint(0, 10**9) for _ in range(N - len(a))]}
