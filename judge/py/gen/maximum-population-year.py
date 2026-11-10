"""Maximum Population Year with the maximum 100 logs spanning the full 1950-2050 range."""

SEEDS = 2


def generate(rng):
    logs = []
    for _ in range(100):
        birth = rng.randint(1950, 2049)
        logs.append([birth, rng.randint(birth + 1, 2050)])
    return {"logs": logs}
