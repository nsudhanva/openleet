"""Last Stone Weight II with the maximum 30 stones, all multiples of g (2 or 6) whose quotients sum
to an odd number, so every split leaves at least g and a sign search that stops at the 0 / 1 lower
bound must still try all 2^30 sign choices."""

SEEDS = 2
N = 30
TOP = 100


def generate(rng):
    g = 2 if rng.random() < 0.5 else 6
    while True:
        quotients = [rng.randint(1, TOP // g) for _ in range(N)]
        # The total is g mod 2g, and flipping a stone's sign moves it by a multiple of 2g.
        if sum(quotients) % 2:
            return {"stones": [g * q for q in quotients]}
