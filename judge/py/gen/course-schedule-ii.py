"""Course Schedule II with 2000 courses and ~10^5 prerequisites built on a Hamiltonian chain,
so the topological order is unique; sometimes one back edge makes it impossible."""

SEEDS = 2
N = 2000
E = 10**5


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
        i = rng.randrange(N // 2)
        pairs.add((order[i], order[rng.randrange(i + 1, N)]))
    prerequisites = [list(p) for p in sorted(pairs)]
    rng.shuffle(prerequisites)
    return {"numCourses": N, "prerequisites": prerequisites}
