"""Sort Items by Groups Respecting Dependencies at n = 2 * 10^4, half the items ungrouped (~10^4
groups to order), with ~6 * 10^4 dependencies along a hidden valid order (one seed closes a
cycle near its end), so a topological sort that rescans for a ready group is ~10^8 steps."""

SEEDS = 2
N = 2 * 10**4
M = 2000
EDGES = 3


def generate(rng):
    # The first draw picks the answer, so seeds 0 and 1 take different branches.
    cyclic = rng.random() < 0.5
    group = [rng.randrange(M) if rng.random() < 0.5 else -1 for _ in range(N)]
    # Lay groups out in a random order, each group's items together, and point every
    # dependency backwards along that layout: a valid order exists.
    keys = {}
    for i, g in enumerate(group):
        keys.setdefault(g if g >= 0 else M + i, []).append(i)
    blocks = list(keys.values())
    rng.shuffle(blocks)
    layout = []
    for items in blocks:
        rng.shuffle(items)
        layout += items
    before = [[] for _ in range(N)]
    for pos in range(1, N):
        item = layout[pos]
        # Mostly the item just before (a long chain of groups), plus a few random earlier ones.
        picks = {layout[pos - 1]}
        for _ in range(rng.randint(0, EDGES)):
            picks.add(layout[rng.randrange(pos)])
        before[item] = sorted(picks)
    if cyclic:
        # A dependency from a late group back to an early one closes a cycle: the answer is [].
        early, late = layout[N - 1 - N // 7], layout[N - 1 - N // 20]
        before[early].append(late)
    return {"n": N, "m": M, "group": group, "beforeItems": before}
