"""Maximum Score After Binary Swaps with 6 * 10^4 random values, mostly zeros in the first half
and ones in the second, so tens of thousands of values wait at once and taking the largest by a
scan is quadratic."""

SEEDS = 2
N = 6 * 10**4


def generate(rng):
    nums = [rng.randint(1, 10**9) for _ in range(N)]
    s = "".join("1" if rng.random() < (0.1 if i < N // 2 else 0.9) else "0" for i in range(N))
    return {"nums": nums, "s": s}
