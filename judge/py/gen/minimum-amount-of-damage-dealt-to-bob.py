"""Minimum Amount of Damage Dealt to Bob with 2 * 10^4 enemies, so choosing each next enemy by
scanning all the living ones is quadratic."""

SEEDS = 2
N = 2 * 10**4
LIMIT = 10**4


def generate(rng):
    damage = [rng.randint(1, LIMIT) for _ in range(N)]
    health = [rng.randint(1, LIMIT) for _ in range(N)]
    return {"power": rng.randint(1, 100), "damage": damage, "health": health}
