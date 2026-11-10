"""Loud and Rich at n = 500 with a consistent (acyclic) richer relation: a dense random order
with tens of thousands of edges, or one long chain 500 deep."""

SEEDS = 2
N = 500


def generate(rng):
    rank = list(range(N))
    rng.shuffle(rank)  # rank[i] = position of person i, richest first
    by_rank = sorted(range(N), key=lambda p: rank[p])
    richer = []
    if rng.random() < 0.5:
        for i in range(N):
            for j in range(i + 1, N):
                if rng.random() < 0.3:
                    richer.append([by_rank[i], by_rank[j]])
    else:
        richer = [[by_rank[i], by_rank[i + 1]] for i in range(N - 1)]
    rng.shuffle(richer)
    quiet = list(range(N))
    rng.shuffle(quiet)
    return {"richer": richer, "quiet": quiet}
