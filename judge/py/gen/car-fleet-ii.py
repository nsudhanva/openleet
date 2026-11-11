"""Car Fleet II at n = 2 * 10^4: speeds rise toward the front and the front car is the slowest,
so every car catches up only with the front fleet and scanning ahead car by car is quadratic."""

SEEDS = 2
N = 2 * 10**4
LIMIT = 10**6


def generate(rng):
    positions = sorted(rng.sample(range(1, LIMIT + 1), N))
    speeds = sorted(rng.sample(range(2, LIMIT + 1), N - 1))
    speeds.append(1)
    return {"cars": [[p, s] for p, s in zip(positions, speeds, strict=True)]}
