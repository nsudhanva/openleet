"""Insufficient Nodes in Root to Leaf Paths at the maximum 5000 nodes: a comb (a 2500-node spine
with one leaf off every spine node) with leaf sums growing with depth and the limit at the median,
so half the leaves are pruned and walking up from every leaf costs ~3 * 10^6 steps; 16 seeds
add up the ~150 ms each of those walks past the 1 s floor."""

from _shapes import leaf_sums, level_order, pick_shape

SEEDS = 16
N = 5000


def generate(rng):
    # Shapes: every leaf on the left, every leaf on the right, or random sides and spine values.
    # One-sided leaves make leaf sums rise (right) or fall (left) with depth, in the order a
    # stack walk lists the leaves, so a walk up from each leaf that stops at a better ancestor
    # still runs to the root.
    shape = pick_shape(rng)
    spine = N // 2
    left, right = [None] * N, [None] * N
    for i in range(spine):
        leaf = spine + i
        child = i + 1 if i + 1 < spine else None
        if shape == 0 or (shape == 2 and rng.random() < 0.5):
            left[i], right[i] = leaf, child
        else:
            left[i], right[i] = child, leaf
    if shape == 2:
        vals = [rng.randint(-100, 100) for _ in range(spine)]
    elif shape == 0:
        vals = [rng.randint(-100, -1) for _ in range(spine)]
    else:
        vals = [rng.randint(1, 100) for _ in range(spine)]
    vals += [rng.randint(0, 50) for _ in range(N - spine)]
    sums = sorted(leaf_sums(vals, left, right))
    return {"root": level_order(vals, left, right), "limit": sums[len(sums) // 2]}
