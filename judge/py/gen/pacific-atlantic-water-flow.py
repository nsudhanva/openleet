"""Pacific Atlantic on a 200 x 200 grid: random heights, or a smooth ridge where most cells
reach both oceans and a per-cell search is quadratic."""

SEEDS = 2
SIZE = 200


def generate(rng):
    if rng.random() < 0.5:
        heights = [[rng.randint(0, 10**5) for _ in range(SIZE)] for _ in range(SIZE)]
    else:
        heights = [
            [min(r, c, SIZE - 1 - r, SIZE - 1 - c) * 100 + rng.randint(0, 1) for c in range(SIZE)]
            for r in range(SIZE)
        ]
    return {"heights": heights}
