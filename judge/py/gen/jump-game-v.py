"""Jump Game V at the maximum n = 1000 with d at least 3n / 4: a strictly descending staircase or
a single strict mountain, so every index reaches long chains of lower ones; a search without
memoization branches exponentially and re-checking the heights between i and j per jump is
O(n d^2)."""

SEEDS = 2
N = 1000
TOP = 10**5


def generate(rng):
    heights = sorted(rng.sample(range(1, TOP + 1), N), reverse=True)
    if rng.random() < 0.5:
        arr = heights
    else:
        # The tallest in the middle, the rest falling away on both sides.
        peak = rng.randrange(N // 4, 3 * N // 4)
        left = sorted(rng.sample(heights[1:], peak))
        rest = sorted(set(heights[1:]) - set(left), reverse=True)
        arr = [*left, heights[0], *rest]
    d = rng.randint(3 * N // 4, N)
    return {"arr": arr, "d": d}
