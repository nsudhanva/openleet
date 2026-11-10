"""Delete Nodes And Return Forest on a 1000-node tree (values 1..1000): a random tree or a
long chain, deleting a random subset that splits it into many pieces."""

from collections import deque

SEEDS = 2
N = 1000


def level_order(vals, left, right):
    out, q = [], deque([0])
    while q:
        u = q.popleft()
        if u < 0:
            out.append(None)
            continue
        out.append(vals[u])
        q.append(left[u])
        q.append(right[u])
    while out[-1] is None:
        out.pop()
    return out


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
    return {"root": level_order(vals, left, right), "to_delete": to_delete}
