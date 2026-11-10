"""Maximum Path Score on a 200 x 200 grid of 0 / 1 / 2 with k up to 1000 (grid[0][0] = 0), so
the state space is about 4 * 10^7 if done naively."""

SEEDS = 3
N = 200


def generate(rng):
    m, n = rng.choice([(200, 200), (200, 200), (1, 200), (200, 3)])
    grid = [[rng.randint(0, 2) for _ in range(n)] for _ in range(m)]
    grid[0][0] = 0
    k = rng.choice([0, 10**3, rng.randint(0, 10**3), rng.randint(0, 50)])
    return {"grid": grid, "k": k}
