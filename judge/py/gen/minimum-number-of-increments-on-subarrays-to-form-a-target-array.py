"""Minimum Number of Increments on Subarrays to Form a Target Array at n = 2 * 10^4: a noisy
ramp (rising on one seed, falling on the other), so splitting at the minimum and recursing peels
one element per level, ~2 * 10^8 steps."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    step = 10**5 // N
    target = [1 + step * i + rng.randint(0, step - 1) for i in range(N)]
    if rng.random() < 0.5:
        target.reverse()
    return {"target": target}
