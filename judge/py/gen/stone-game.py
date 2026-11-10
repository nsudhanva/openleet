"""Stone Game at the maximum 500 piles with values up to 500 and an odd total."""

SEEDS = 2


def generate(rng):
    piles = [rng.randint(1, 500) for _ in range(500)]
    if sum(piles) % 2 == 0:
        piles[0] += 1 if piles[0] < 500 else -1
    return {"piles": piles}
