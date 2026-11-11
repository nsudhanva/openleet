"""Separate Black and White Balls at n = 2 * 10^4, mostly all 1s before all 0s (about 10^8
inversions), so swapping adjacent pairs one at a time does on the order of n^2 steps."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    noise = rng.choice([0.02, 0.2])
    half = N // 2
    s = [
        ("0" if rng.random() < noise else "1")
        if i < half
        else ("1" if rng.random() < noise else "0")
        for i in range(N)
    ]
    return {"s": "".join(s)}
