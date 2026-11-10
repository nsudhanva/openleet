"""Making a Large Island on a 500 x 500 grid: mostly land with scattered zeros (re-flooding
per zero is quartic), a checkerboard, or random cells."""

SEEDS = 3
N = 500


def generate(rng):
    shape = rng.choice(["land", "checker", "random"])
    if shape == "land":
        grid = [[0 if rng.random() < 0.05 else 1 for _ in range(N)] for _ in range(N)]
    elif shape == "checker":
        grid = [[(r + c) % 2 for c in range(N)] for r in range(N)]
    else:
        grid = [[rng.randint(0, 1) for _ in range(N)] for _ in range(N)]
    return {"grid": grid}
