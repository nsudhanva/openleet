"""Maximize Sum Of Array After K Negations at the limits n = k = 10^4, so flipping the current
minimum k times with a fresh scan each time is 2 * 10^8 element visits."""

SEEDS = 2
N = 10**4


def generate(rng):
    nums = [rng.randint(-100, 100) for _ in range(N)]
    return {"nums": nums, "k": N}
