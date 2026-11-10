"""Redundant Connection at n = 1000: a random or path-like tree plus one extra edge closing a
long cycle, shuffled so the redundant edge can be anywhere."""

SEEDS = 2
N = 1000


def generate(rng):
    label = list(range(1, N + 1))
    rng.shuffle(label)
    deep = rng.random() < 0.5
    edges = set()
    for v in range(1, N):
        p = rng.randint(max(0, v - 2), v - 1) if deep else rng.randrange(v)
        a, b = label[p], label[v]
        edges.add((min(a, b), max(a, b)))
    while True:
        a, b = rng.sample(label, 2)
        e = (min(a, b), max(a, b))
        if e not in edges:
            edges.add(e)
            break
    out = [list(e) for e in sorted(edges)]
    rng.shuffle(out)
    return {"edges": out}
