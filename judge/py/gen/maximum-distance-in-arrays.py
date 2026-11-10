"""Maximum Distance in Arrays with 10^5 integers in total: 10^5 one-element arrays (quadratic
pairing times out), or 200 arrays of 500 with the global min and max in the same array."""

SEEDS = 2
LIMIT = 10**4


def generate(rng):
    if rng.random() < 0.5:
        arrays = [[rng.randint(-LIMIT, LIMIT)] for _ in range(10**5)]
    else:
        arrays = [
            sorted(rng.randint(-LIMIT // 2, LIMIT // 2) for _ in range(500)) for _ in range(200)
        ]
        host = rng.randrange(200)
        arrays[host][0] = -LIMIT
        arrays[host][-1] = LIMIT
    return {"arrays": arrays}
