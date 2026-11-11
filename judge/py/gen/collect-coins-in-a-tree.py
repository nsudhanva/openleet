"""Collect Coins in a Tree at n = 10^4: a long caterpillar-like tree with sparse or dense coins
and a coinless path of n / 2 nodes hanging off it, so trying every start vertex costs ~n^2 steps
and stripping coinless leaves one layer per full scan takes n / 2 scans."""

SEEDS = 2
N = 10**4
TAIL = N // 2


def generate(rng):
    chain = rng.choice((0.7, 0.95))
    density = rng.choice((0.03, 0.3))
    body = N - TAIL
    edges = []
    for v in range(1, body):
        parent = v - 1 if rng.random() < chain else rng.randrange(v)
        edges.append([parent, v])
    edges.append([rng.randrange(body), body])
    edges += [[v - 1, v] for v in range(body + 1, N)]
    coins = [int(v < body and rng.random() < density) for v in range(N)]
    labels = list(range(N))
    rng.shuffle(labels)
    edges = [
        [labels[a], labels[b]] if rng.random() < 0.5 else [labels[b], labels[a]] for a, b in edges
    ]
    rng.shuffle(edges)
    shuffled = [0] * N
    for v in range(N):
        shuffled[labels[v]] = coins[v]
    return {"coins": shuffled, "edges": edges}
