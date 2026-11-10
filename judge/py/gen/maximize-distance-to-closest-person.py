"""Maximize Distance to Closest Person on 2 * 10^4 seats: sparse occupants with the widest gap
at an edge or in the middle."""

SEEDS = 3
N = 2 * 10**4


def generate(rng):
    shape = rng.choice(["sparse", "edge", "dense"])
    if shape == "edge":
        seats = [0] * N
        seats[rng.randint(N // 2, N - 1)] = 1
        if rng.random() < 0.5:
            seats.reverse()
    elif shape == "sparse":
        seats = [1 if rng.random() < 0.001 else 0 for _ in range(N)]
        seats[rng.randrange(N)] = 1
    else:
        seats = [1 if rng.random() < 0.9 else 0 for _ in range(N)]
        seats[rng.randrange(N)] = 0
        seats[rng.randrange(N)] = 1
        if all(seats):
            seats[0] = 0
    return {"seats": seats}
