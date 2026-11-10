"""Reverse Pairs at n = 5 * 10^4: full 32-bit range (overflow traps) or strictly decreasing so
nearly every pair counts and a quadratic scan does ~1.25 * 10^9 checks."""

SEEDS = 3
N = 5 * 10**4
LO, HI = -(2**31), 2**31 - 1


def generate(rng):
    shape = rng.getrandbits(6) % 3
    if shape == 0:
        return {"nums": [rng.randint(LO, HI) for _ in range(N)]}
    if shape == 1:
        return {"nums": sorted((rng.randint(LO, HI) for _ in range(N)), reverse=True)}
    # Extreme values only: 2 * nums[j] overflows 32 bits.
    return {"nums": [rng.choice([LO, HI, HI // 2, HI // 2 + 1, -1, 0]) for _ in range(N)]}
