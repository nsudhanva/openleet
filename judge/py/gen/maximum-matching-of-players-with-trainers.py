"""Maximum Matching of Players With Trainers with 3 * 10^4 players and trainers of random
abilities, so matching each sorted player by rescanning the trainers is quadratic."""

SEEDS = 2
N = 3 * 10**4
LIMIT = 10**9


def generate(rng):
    players = [rng.randint(1, LIMIT) for _ in range(N)]
    trainers = [rng.randint(1, LIMIT) for _ in range(N)]
    return {"players": players, "trainers": trainers}
