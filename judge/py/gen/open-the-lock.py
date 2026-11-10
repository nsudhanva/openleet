"""Open the Lock with 500 distinct deadends and a far target, so BFS explores most of the
10^4 states."""

SEEDS = 2


def generate(rng):
    target = "".join(rng.choice("456") for _ in range(4))
    pool = [f"{i:04d}" for i in range(1, 10**4) if f"{i:04d}" != target]
    deadends = rng.sample(pool, 500)
    return {"deadends": deadends, "target": target}
