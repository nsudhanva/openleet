"""Stable Subarrays With Equal Boundary and Interior Sum at n = 2 * 10^4 drawn from a few small
values (or long zero runs), so many subarrays are stable and checking every (l, r) pair is
~2 * 10^8 steps."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    if rng.random() < 0.5:
        capacity = [rng.choice((-2, -1, 0, 0, 1, 2)) for _ in range(N)]
    else:
        capacity = [0 if rng.random() < 0.8 else rng.randint(-(10**9), 10**9) for _ in range(N)]
    return {"capacity": capacity}
