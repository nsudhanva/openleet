"""Bounded Maximum at n = 10^5: long stretches inside [left, right] so the answer is huge and
a quadratic scan is too slow."""

SEEDS = 2
N = 10**5


def generate(rng):
    if rng.random() < 0.5:
        left, right = 10**8, 9 * 10**8
        nums = [rng.randint(0, 10**9) for _ in range(N)]
    else:
        left, right = 1000, 2000
        nums = [rng.randint(0, 2000) if rng.random() < 0.9999 else 10**9 for _ in range(N)]
    return {"nums": nums, "left": left, "right": right}
