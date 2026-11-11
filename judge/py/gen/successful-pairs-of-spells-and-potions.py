"""Successful Pairs of Spells and Potions with 2 * 10^4 spells and potions, so testing every
pair is 4 * 10^8 products."""

SEEDS = 2
N = 2 * 10**4
LIMIT = 10**5


def generate(rng):
    spells = [rng.randint(1, LIMIT) for _ in range(N)]
    potions = [rng.randint(1, LIMIT) for _ in range(N)]
    return {"spells": spells, "potions": potions, "success": rng.randint(10**8, 5 * 10**9)}
