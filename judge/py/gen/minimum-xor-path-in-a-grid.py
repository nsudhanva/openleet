"""Minimum XOR Path at 16 x 16 with random values below 1024, so tracking the reachable XOR set
per cell is ~2.6 * 10^5 steps while walking every one of the C(30, 15) ~ 1.6 * 10^8 monotone
paths never finishes."""

SEEDS = 2
M = 16


def generate(rng):
    return {"grid": [[rng.randrange(1024) for _ in range(M)] for _ in range(M)]}
