"""Number of Ways to Split Array at 5 * 10^4 values, so summing both sides afresh at every split
costs 2.5 * 10^9 additions."""

SEEDS = 2
N = 5 * 10**4
TOP = 10**5


def generate(rng):
    shift = rng.randint(-TOP // 10, TOP // 10)
    nums = [max(-TOP, min(TOP, rng.randint(-TOP, TOP) + shift)) for _ in range(N)]
    return {"nums": nums}
