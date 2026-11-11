"""Maximum Fruits Harvested After at Most K Steps with 2 * 10^4 fruit positions in [0, 2 * 10^5]
and k up to a quarter of the axis, so trying every reachable pair of end fruits is ~2 * 10^8
checks."""

SEEDS = 2
N = 2 * 10**4
SPAN = 2 * 10**5


def generate(rng):
    positions = sorted(rng.sample(range(SPAN + 1), N))
    return {
        "fruits": [[p, rng.randint(1, 10**4)] for p in positions],
        "startPos": rng.randint(SPAN // 4, 3 * SPAN // 4),
        "k": rng.randint(SPAN // 8, SPAN // 4),
    }
