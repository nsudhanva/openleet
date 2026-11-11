"""Maximum Sum of 3 Non-Overlapping Subarrays at the maximum n = 2 * 10^4: k from 5 to 20 (random
values, or {1, 2} with k >= 16 so many windows tie below the 6k bound) where searching the best
left and right window for every middle one is ~10^9 steps, or k near n / 4 where summing every
window afresh is ~7 * 10^7 steps."""

from _shapes import pick_shape

SEEDS = 3
N = 2 * 10**4
TOP = 2**16 - 1


def generate(rng):
    shape = pick_shape(rng)
    if shape == 0:
        return {"nums": [rng.randint(1, TOP) for _ in range(N)], "k": rng.randint(5, 20)}
    if shape == 1:
        return {"nums": [rng.randint(1, 2) for _ in range(N)], "k": rng.randint(16, 20)}
    return {"nums": [rng.randint(1, TOP) for _ in range(N)], "k": rng.randint(N // 5, N // 4)}
