"""Maximum White Tiles Covered by a Carpet at n = 3 * 10^4 shuffled tiles and a carpet spanning
half the floor, so summing the tiles under each placement afresh costs ~2 * 10^8 steps."""

SEEDS = 2
N = 3 * 10**4
LIMIT = 10**9


def generate(rng):
    points = sorted(rng.sample(range(1, LIMIT + 1), 2 * N))
    tiles = [[points[2 * i], points[2 * i + 1]] for i in range(N)]
    rng.shuffle(tiles)
    span = points[-1] - points[0]
    return {"tiles": tiles, "carpetLen": rng.randint(span * 2 // 5, span * 3 // 5)}
