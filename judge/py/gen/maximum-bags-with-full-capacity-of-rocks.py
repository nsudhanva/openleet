"""Maximum Bags With Full Capacity of Rocks at n = 5 * 10^4, most bags needing a few thousand
rocks and enough extra for all but a few of them. Most seeds list the bags from the most to the
least needed, so building a sorted list with bisect.insort moves ~5 * 10^4 items per bag; the
others are shuffled. Picking the emptiest remaining bag by a scan each time is ~10^9 steps."""

from _shapes import pick_shape

SEEDS = 5
N = 5 * 10**4
NEED = 3 * 10**4
LIMIT = 10**9


def generate(rng):
    needs = [rng.randint(0, NEED) for _ in range(N)]
    if pick_shape(rng) == 1:
        rng.shuffle(needs)
    else:
        needs.sort(reverse=True)
    capacity, rocks = [], []
    for need in needs:
        cap = rng.randint(max(need, 1), LIMIT)
        capacity.append(cap)
        rocks.append(cap - need)
    extra = max(1, sum(sorted(needs)[: N - rng.randint(1, 10)]))
    return {"capacity": capacity, "rocks": rocks, "additionalRocks": extra}
