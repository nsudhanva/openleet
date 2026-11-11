"""Number of Operations to Make Network Connected at 5 * 10^4 computers and ~5 * 10^4 cables: a hub
whose 3 * 10^4 cables alternate which end names the hub, then small groups and spare cables, so a
union-find without path compression or union by size walks a chain that grows with every cable."""

SEEDS = 2
N = 5 * 10**4
HUB = 3 * 10**4


def generate(rng):
    ids = rng.sample(range(N), N)
    hub = ids[:HUB]
    edges = [[hub[0], hub[i]] if i % 2 else [hub[i], hub[0]] for i in range(1, HUB)]
    rest, used = [], set()
    others = ids[HUB:]
    for k in range(1, len(others)):
        if rng.random() < 0.7:
            rest.append([others[rng.randrange(k)], others[k]])
    groups = len(others) - len(rest)
    while len(edges) + len(rest) < N - 1 + rng.randrange(N // 25):
        a, b = rng.sample(range(1, HUB), 2)
        if (min(a, b), max(a, b)) not in used:
            used.add((min(a, b), max(a, b)))
            rest.append([hub[a], hub[b]])
    assert groups > 0
    rng.shuffle(rest)
    return {"n": N, "connections": edges + rest}
