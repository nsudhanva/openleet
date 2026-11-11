"""Number of Good Leaf Nodes Pairs at the maximum 1,024 nodes as a caterpillar: a 512-node spine
with a leaf on every spine node, so pairing every two of the 512 leaves and walking up to their
common ancestor costs ~2 * 10^7 steps."""

from _shapes import level_order

SEEDS = 2
N = 1024


def generate(rng):
    spine = N // 2
    left, right = [None] * N, [None] * N
    for i in range(spine):
        leaf = spine + i
        if rng.random() < 0.5:
            left[i], right[i] = leaf, (i + 1 if i + 1 < spine else None)
        else:
            left[i], right[i] = (i + 1 if i + 1 < spine else None), leaf
    vals = [rng.randint(1, 100) for _ in range(N)]
    return {"root": level_order(vals, left, right), "distance": rng.randint(6, 10)}
