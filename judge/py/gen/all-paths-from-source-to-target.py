"""All Paths From Source to Target at n = 15: the complete DAG (2^13 paths) or a dense random
DAG, with adjacency lists shuffled."""

SEEDS = 2
N = 15


def generate(rng):
    p = 1.0 if rng.random() < 0.5 else 0.8
    graph = []
    for i in range(N):
        out = [j for j in range(i + 1, N) if rng.random() < p]
        rng.shuffle(out)
        graph.append(out)
    return {"graph": graph}
