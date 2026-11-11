"""Maximum Building Height with n = 10^9 and 2 * 10^4 unsorted restrictions far below the
gaps' reach, so relaxing every restriction against every other is 4 * 10^8 steps."""

SEEDS = 2
N = 10**9
R = 2 * 10**4


def generate(rng):
    ids = rng.sample(range(2, N + 1), R)
    reach = N // R * 2
    return {"n": N, "restrictions": [[i, rng.randint(0, reach)] for i in ids]}
