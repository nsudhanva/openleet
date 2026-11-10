"""Heaters with 3 * 10^4 houses and heaters up to 10^9, unsorted; heaters clustered so some
houses are very far from the nearest one."""

SEEDS = 3
N = 3 * 10**4


def generate(rng):
    houses = [rng.randint(1, 10**9) for _ in range(N)]
    shape = rng.randrange(3)
    if shape == 0:
        heaters = [rng.randint(1, 10**9) for _ in range(N)]
    elif shape == 1:
        heaters = [rng.randint(1, 1000) for _ in range(rng.choice([1, N]))]
    else:
        heaters = houses[:]
        rng.shuffle(heaters)
        heaters[0] = 10**9
    return {"houses": houses, "heaters": heaters}
