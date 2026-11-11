"""Separate Black and White Balls at n = 10^5, mostly 1s in the first 70-80 % and mostly 0s after
(about 3 * 10^9 inversions), so swapping adjacent pairs one at a time does on the order of n^2
steps, and counting the 0s to the right of every 1 scans ~4 * 10^9 characters."""

SEEDS = 2
N = 10**5


def generate(rng):
    noise = rng.choice([0.02, 0.2])
    split = N * rng.randint(70, 80) // 100
    s = [
        ("0" if rng.random() < noise else "1")
        if i < split
        else ("1" if rng.random() < noise else "0")
        for i in range(N)
    ]
    return {"s": "".join(s)}
