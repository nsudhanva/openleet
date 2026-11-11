"""Divide Array Into Increasing Sequences at n = 10^5 with k right at or just past n / f, where f
is the largest count: either ~10^5 distinct values and one repeated 20 to 40 times, so counting
each value by a scan is ~6 * 10^9 comparisons, or one value repeated ~6 * 10^4 times, so
measuring the run from every index is ~2 * 10^9 steps."""

from _shapes import pick_shape

SEEDS = 3
N = 10**5


def generate(rng):
    shape = pick_shape(rng)
    f = rng.randint(N * 11 // 20, N * 13 // 20) if shape == 1 else rng.randint(20, 40)
    values = rng.sample(range(1, 10**5 + 1), N - f + 1)
    big = values.pop()
    nums = sorted(values + [big] * f)
    k = N // f + (shape == 2)  # shape 2 just fails: f * k > n
    return {"nums": nums, "k": k}
