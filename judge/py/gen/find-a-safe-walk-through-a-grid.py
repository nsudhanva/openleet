"""Find a Safe Walk on a 50 x 50 grid with many unsafe cells and health just around what the
cheapest path needs."""

SEEDS = 2
SIZE = 50


def generate(rng):
    p = rng.choice([0.3, 0.5])
    grid = [[1 if rng.random() < p else 0 for _ in range(SIZE)] for _ in range(SIZE)]
    health = rng.randint(1, 2 * SIZE)
    return {"grid": grid, "health": health}
