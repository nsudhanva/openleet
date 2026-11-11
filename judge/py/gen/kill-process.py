"""Kill Process at n = 5 * 10^4 (a chain, a random tree or two shallow bushy halves) killing the
process whose subtree holds about half of them, so finding each victim's children by scanning
every process costs ~10^9 steps."""

from _shapes import pick_shape

SEEDS = 3
N = 5 * 10**4


def generate(rng):
    shape = pick_shape(rng)
    ids = rng.sample(range(1, 5 * 10**4 + 1), N)
    parent = [-1]
    for v in range(1, N):
        if shape == 0:
            parent.append(v - 1)
        elif shape == 1:
            parent.append(rng.randrange(v))
        elif v <= 2:
            parent.append(0)
        else:
            # Odd nodes hang below node 1 and even ones below node 2, at most a few levels deep.
            parent.append(rng.randrange(2 - v % 2, min(v, 60), 2))
    size = [1] * N
    for v in range(N - 1, 0, -1):
        size[parent[v]] += size[v]
    victim = min(range(1, N), key=lambda v: abs(2 * size[v] - N)) if N > 1 else 0
    pid = ids[:]
    ppid = [0] + [ids[p] for p in parent[1:]]
    order = list(range(N))
    rng.shuffle(order)
    return {"pid": [pid[i] for i in order], "ppid": [ppid[i] for i in order], "kill": ids[victim]}
