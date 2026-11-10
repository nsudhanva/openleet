"""Delete Nodes And Return Forest on a 1000-node tree (values 1..1000): a random tree or a
long chain, deleting a random subset that splits it into many pieces."""

from _shapes import level_order

SEEDS = 2
N = 1000


def generate(rng):
    vals = rng.sample(range(1, N + 1), N)
    left, right = [-1] * N, [-1] * N
    if rng.random() < 0.5:
        for i in range(1, N):
            (left if rng.random() < 0.5 else right)[i - 1] = i
    else:
        slots = [(0, 0), (0, 1)]
        for i in range(1, N):
            j = rng.randrange(len(slots))
            slots[j], slots[-1] = slots[-1], slots[j]
            p, side = slots.pop()
            (left if side == 0 else right)[p] = i
            slots += [(i, 0), (i, 1)]
    to_delete = rng.sample(range(1, N + 1), rng.randint(50, 400))
    return {"root": level_order(vals, left, right, empty=-1), "to_delete": to_delete}
