"""Find All Lonely Numbers at n = 10^5 over [0, 10^6]: random, or values clustered tightly so
most have neighbours or duplicates."""

SEEDS = 2
N = 10**5


def generate(rng):
    if rng.random() < 0.5:
        nums = [rng.randint(0, 10**6) for _ in range(N)]
    else:
        nums = [
            2 * rng.randint(0, 5 * 10**5) if rng.random() < 0.8 else rng.randint(0, 10**6)
            for _ in range(N)
        ]
    return {"nums": nums}
