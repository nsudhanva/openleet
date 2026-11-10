"""Next Greater Element II at n = 10^4: strictly decreasing (each answer wraps all the way
around), all equal (all -1), or random."""

SEEDS = 3
N = 10**4


def generate(rng):
    kind = rng.choice(("decreasing", "equal", "random"))
    if kind == "decreasing":
        nums = sorted(rng.sample(range(-(10**9), 10**9 + 1), N), reverse=True)
    elif kind == "equal":
        nums = [rng.randint(-(10**9), 10**9)] * N
    else:
        nums = [rng.randint(-(10**9), 10**9) for _ in range(N)]
    return {"nums": nums}
