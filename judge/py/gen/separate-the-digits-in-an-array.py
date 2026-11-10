"""Separate the Digits on 1000 numbers in [1, 10^5], many of them 5- and 6-digit."""

SEEDS = 2


def generate(rng):
    return {
        "nums": [
            rng.choice([rng.randint(1, 10**5), 10**5, rng.randint(10**4, 10**5)])
            for _ in range(1000)
        ]
    }
