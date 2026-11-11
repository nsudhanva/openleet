"""Find the Kth Smallest Sum of a Matrix With Sorted Rows at 40 x 40 with k = 200, so merging
the rows without trimming to the k smallest grows as 40^m."""

SEEDS = 2
M = 40
N = 40
K = 200


def generate(rng):
    top = rng.choice((5000, 50))
    mat = [sorted(rng.randint(1, top) for _ in range(N)) for _ in range(M)]
    return {"mat": mat, "k": min(K, N**M)}
