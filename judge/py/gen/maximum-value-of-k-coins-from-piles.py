"""Maximum Value of K Coins From Piles at the maximum 1000 piles and 2000 coins with k = 1500, so
a knapsack that tries every count up to j for each pile costs ~10^9 steps."""

SEEDS = 2
PILES = 1000
COINS = 2000
K = 1500


def generate(rng):
    sizes = [1] * PILES
    for _ in range(COINS - PILES):
        sizes[rng.randrange(PILES)] += 1
    piles = [[rng.randint(1, 10**5) for _ in range(s)] for s in sizes]
    return {"piles": piles, "k": K}
