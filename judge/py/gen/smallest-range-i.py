"""Smallest Range I on 10^4 values in [0, 10^4] with k small or large."""

SEEDS = 2


def generate(rng):
    return {
        "nums": [rng.randint(0, 10**4) for _ in range(10**4)],
        "k": rng.choice([rng.randint(0, 100), rng.randint(0, 10**4)]),
    }
