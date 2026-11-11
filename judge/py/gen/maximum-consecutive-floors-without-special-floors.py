"""Maximum Consecutive Floors Without Special Floors with 2 * 10^4 unsorted special floors over
~10^9 floors, so finding each one's next special floor by a scan is 4 * 10^8 steps."""

SEEDS = 2
N = 2 * 10**4
TOP = 10**9


def generate(rng):
    bottom = rng.randint(1, 1000)
    top = rng.randint(TOP - 1000, TOP)
    return {"bottom": bottom, "top": top, "special": rng.sample(range(bottom, top + 1), N)}
