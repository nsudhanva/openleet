"""Max Area of Island on the maximum 50 x 50 grid, nearly all land with a few scattered holes, so
one island holds ~2400 cells and flood-filling afresh from every land cell is ~6 * 10^6 visits."""

SEEDS = 2
N = 50


def generate(rng):
    holes = rng.choice([0.02, 0.08])
    grid = [[0 if rng.random() < holes else 1 for _ in range(N)] for _ in range(N)]
    return {"grid": grid}
