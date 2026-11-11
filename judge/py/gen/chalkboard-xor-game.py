"""Chalkboard XOR Game at the maximum 1000 (or 999) distinct-drawn values below 2^16 whose XOR
is not zero, so the game is not over at the start and a search over the moves blows up."""

SEEDS = 2
N = 1000


def generate(rng):
    nums = rng.sample(range(2**16), N - (rng.random() < 0.5))
    x = 0
    for v in nums:
        x ^= v
    if x == 0:
        nums[-1] ^= 1 if nums[-1] ^ 1 not in nums else 2
    return {"nums": nums}
