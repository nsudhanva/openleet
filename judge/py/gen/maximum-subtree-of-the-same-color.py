"""Maximum Subtree of the Same Color at n = 3 * 10^4: a path from node 0 through shuffled labels,
one colour except a different colour halfway down, so walking each node's subtree, even with an
early exit on a mismatch, costs ~10^8 steps."""

SEEDS = 2
N = 3 * 10**4


def generate(rng):
    order = [0, *rng.sample(range(1, N), N - 1)]
    edges = [
        [order[i], order[i + 1]] if rng.random() < 0.5 else [order[i + 1], order[i]]
        for i in range(N - 1)
    ]
    rng.shuffle(edges)
    color = rng.randint(1, 10**5)
    colors = [color] * N
    cut = N // 2 + rng.randint(-(N // 300), N // 300)
    colors[order[cut]] = color % 10**5 + 1
    return {"edges": edges, "colors": colors}
