"""Minimum Common Value at 10^5 sorted values each: the only common value is the largest in nums2,
or no common value at all (odds against evens), so a nested scan is 10^10 steps."""

SEEDS = 3
N = 10**5


def generate(rng):
    a = sorted(rng.randint(1, 5 * 10**8 - 1) * 2 for _ in range(N))
    b = sorted(rng.randint(0, 5 * 10**8 - 1) * 2 + 1 for _ in range(N))
    if rng.random() < 0.7:
        a[-1] = b[-1]
        a.sort()
    return {"nums1": a, "nums2": b}
