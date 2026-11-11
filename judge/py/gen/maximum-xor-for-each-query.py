"""Maximum XOR for Each Query at n = 3 * 10^4, so XOR-ing the remaining prefix afresh for every
query costs ~4.5 * 10^8 steps."""

SEEDS = 2
N = 3 * 10**4


def generate(rng):
    bits = rng.randint(15, 20)
    return {"nums": sorted(rng.randrange(1 << bits) for _ in range(N)), "maximumBit": bits}
