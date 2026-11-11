"""Possible Bipartition at n = 2000 with 10^4 unique dislikes: a hidden bipartite split (true),
or the same plus one same-side edge between two of the nodes a BFS from person 1 reaches last
(false), so scanning every dislike per visited person is ~2 * 10^7 steps."""

from _shapes import pick_shape

SEEDS = 3
N = 2000
M = 10**4


def generate(rng):
    odd = pick_shape(rng) == 1
    side = [v % 2 for v in range(N + 1)]
    rng.shuffle(side)
    pairs = set()
    while len(pairs) < M - odd:
        a, b = rng.randint(1, N), rng.randint(1, N)
        if a != b and side[a] != side[b]:
            pairs.add((min(a, b), max(a, b)))
    if odd:
        adj = [[] for _ in range(N + 1)]
        for a, b in sorted(pairs):
            adj[a].append(b)
            adj[b].append(a)
        order, seen = [1], {1}
        for u in order:
            for v in adj[u]:
                if v not in seen:
                    seen.add(v)
                    order.append(v)
        late = order[-len(order) // 10 :] if len(order) > 200 else list(range(1, N + 1))
        while True:
            a, b = sorted(rng.sample(late, 2))
            if side[a] == side[b] and (a, b) not in pairs:
                break
        pairs.add((a, b))
    dislikes = [list(p) for p in sorted(pairs)]
    rng.shuffle(dislikes)
    return {"n": N, "dislikes": dislikes}
