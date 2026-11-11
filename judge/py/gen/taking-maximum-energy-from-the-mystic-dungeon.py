"""Taking Maximum Energy From the Mystic Dungeon at n = 10^5 with k = 1 or 2, so summing the jumps
from every start separately is ~2.5 * 10^9 steps."""

SEEDS = 2
N = 10**5


def generate(rng):
    return {"energy": [rng.randint(-1000, 1000) for _ in range(N)], "k": rng.randint(1, 2)}
