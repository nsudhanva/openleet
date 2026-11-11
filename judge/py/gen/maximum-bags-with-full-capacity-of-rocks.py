"""Maximum Bags With Full Capacity of Rocks at n = 2 * 10^4 with enough extra rocks for all but
a few bags, so picking the emptiest remaining bag by a scan each time is ~2 * 10^8 steps."""

SEEDS = 2
N = 2 * 10**4
NEED = 5 * 10**4
LIMIT = 10**9


def generate(rng):
    capacity, rocks = [], []
    for _ in range(N):
        cap = rng.randint(NEED, LIMIT)
        capacity.append(cap)
        rocks.append(cap - rng.randint(0, NEED))
    needs = sorted(c - r for c, r in zip(capacity, rocks, strict=True))
    extra = max(1, sum(needs[: N - rng.randint(1, 10)]))
    return {"capacity": capacity, "rocks": rocks, "additionalRocks": extra}
