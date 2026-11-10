"""Third Maximum Number at 10^4 values over the full 32-bit range, including only two distinct
values (fall back to the max) and the minimum -2^31 as a real answer."""

SEEDS = 3
N = 10**4
LO, HI = -(2**31), 2**31 - 1


def generate(rng):
    shape = rng.getrandbits(6) % 3  # seeds 0-2 land on three different shapes
    if shape == 0:
        nums = [rng.choice([LO, HI]) for _ in range(N)]
    elif shape == 1:
        nums = [rng.choice([LO, HI, HI - 1]) for _ in range(N)]
    else:
        nums = [rng.randint(LO, HI) for _ in range(N)]
    return {"nums": nums}
