"""Subtree of Another Tree at the maximum sizes (2000 and 1000 nodes): all-equal values where
every candidate matches until a deep leaf, or a real copied subtree, punishing naive matching."""

from _shapes import level_order

SEEDS = 3
N = 2000
M = 1000


def random_tree(rng, n):
    left, right = [None] * n, [None] * n
    slots = [(0, 0), (0, 1)]
    for v in range(1, n):
        j = rng.randrange(len(slots))
        slots[j], slots[-1] = slots[-1], slots[j]
        parent, side = slots.pop()
        (left if side == 0 else right)[parent] = v
        slots.append((v, 0))
        slots.append((v, 1))
    return left, right


def chain(n, vals):
    return level_order(vals, [i + 1 if i + 1 < n else None for i in range(n)], [None] * n, 0)


def generate(rng):
    shape = rng.getrandbits(6) % 3  # seeds 0-2 land on three different shapes
    if shape == 0:
        # Left chains of ones; subRoot ends in 2 so it matches only at the very bottom (or never).
        root_vals = [1] * N
        if rng.random() < 0.5:
            root_vals[-1] = 2
        sub_vals = [1] * M
        sub_vals[-1] = 2
        return {"root": chain(N, root_vals), "subRoot": chain(M, sub_vals)}
    left, right = random_tree(rng, N)
    hi = 1 if shape == 1 else 10**4
    vals = [rng.randint(-hi, hi) for _ in range(N)]
    size = [1] * N
    order = []
    stack = [0]
    while stack:
        node = stack.pop()
        order.append(node)
        for child in (left[node], right[node]):
            if child is not None:
                stack.append(child)
    for node in reversed(order):
        for child in (left[node], right[node]):
            if child is not None:
                size[node] += size[child]
    candidates = [v for v in range(N) if 100 <= size[v] <= M] or [
        v for v in range(N) if size[v] <= M
    ]
    pick = rng.choice(candidates)
    sub = level_order(vals, left, right, pick)
    if rng.random() < 0.5:
        # Perturb one value so the copy no longer matches anywhere (most likely).
        idx = rng.choice([i for i, x in enumerate(sub) if x is not None])
        sub[idx] = sub[idx] + 1 if sub[idx] < 10**4 else sub[idx] - 1
    return {"root": level_order(vals, left, right), "subRoot": sub}
