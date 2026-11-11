"""Maximum Number of Operations to Move Ones to the End on 10^5 random bits, so counting the blocks
of zeros to the right of each one is quadratic."""

SEEDS = 2
N = 10**5


def generate(rng):
    return {"s": "".join(rng.choice("01") for _ in range(N))}
