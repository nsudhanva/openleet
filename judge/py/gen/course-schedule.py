"""Course Schedule with 2000 courses and 5000 unique prerequisites: a DAG containing a
2000-long chain (deep DFS, answer true), or the same with one back edge closing a long
cycle."""

SEEDS = 2
N = 2000
E = 5000


def generate(rng):
    order = list(range(N))
    rng.shuffle(order)
    pairs = set()
    for i in range(N - 1):
        pairs.add((order[i + 1], order[i]))
    while len(pairs) < E - 1:
        i, j = sorted(rng.sample(range(N), 2))
        pairs.add((order[j], order[i]))
    if rng.random() < 0.5:
        pairs.add((order[0], order[N - 1]))
    else:
        while len(pairs) < E:
            i, j = sorted(rng.sample(range(N), 2))
            pairs.add((order[j], order[i]))
    prerequisites = [list(p) for p in sorted(pairs)]
    rng.shuffle(prerequisites)
    return {"numCourses": N, "prerequisites": prerequisites}
