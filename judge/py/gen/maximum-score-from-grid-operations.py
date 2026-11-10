"""Maximum Score From Grid Operations on the largest 100 x 100 grid, dense values up to 10^9
in one seed and sparse in the other; brute force over column heights is exponential."""

SEEDS = 3
N = 100


def generate(rng):
    density = rng.choice((1.0, 0.2))
    grid = [
        [rng.randint(0, 10**9) if rng.random() < density else 0 for _ in range(N)] for _ in range(N)
    ]
    return {"grid": grid}
