"""Frog Jump with 2000 stones: densely packed stones (many reachable jump sizes per stone), or a
reachable triangular path whose last stone may be just out of reach."""

SEEDS = 3
N = 2000


def generate(rng):
    shape = rng.randrange(3)
    if shape == 0:
        stones = [*list(range(N - 1)), N - 2 + rng.choice([1, 60, 64])]
    elif shape == 1:
        stones = sorted({0, 1} | set(rng.sample(range(2, 3 * N), N - 2)))
        while len(stones) < N:
            stones.append(stones[-1] + 1)
    else:
        stones, k = [0, 1], 1
        while len(stones) < N:
            k = max(1, k + rng.choice([-1, 0, 1, 1]))
            stones.append(stones[-1] + k)
        stones[-1] += rng.choice([0, 3])
    return {"stones": stones}
