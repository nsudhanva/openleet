"""Maximum Amount of Money Robot Can Earn on a 30 by 30 grid, a third of it robbers, so trying
every monotone path is C(58, 29) ~ 3 * 10^16 routes."""

SEEDS = 2
M = N = 30


def cell(rng):
    return rng.randint(-1000, -1) if rng.random() < 1 / 3 else rng.randint(0, 1000)


def generate(rng):
    return {"coins": [[cell(rng) for _ in range(N)] for _ in range(M)]}
