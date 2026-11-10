"""Keys and Rooms with n = 1000 and 3000 keys in total: a long chain where each room holds the
next room's key (deep DFS), plus noise keys, sometimes with one link of the chain broken."""

import itertools

SEEDS = 3
N = 1000


def generate(rng):
    order = [0, *rng.sample(range(1, N), N - 1)]
    rooms = [set() for _ in range(N)]
    for a, b in itertools.pairwise(order):
        rooms[a].add(b)
    if rng.random() < 0.5:
        # Break the chain; noise keys only point backwards so the tail stays locked.
        cut = rng.randrange(1, N - 1)
        rooms[order[cut]].clear()
        pos = {room: i for i, room in enumerate(order)}
        total = sum(map(len, rooms))
        while total < 3000:
            a = rng.randrange(N)
            b = order[rng.randrange(pos[a] + 1)] if pos[a] <= cut else rng.randrange(N)
            if b != a and b not in rooms[a]:
                rooms[a].add(b)
                total += 1
    else:
        total = sum(map(len, rooms))
        while total < 3000:
            a, b = rng.randrange(N), rng.randrange(N)
            if b != a and b not in rooms[a]:
                rooms[a].add(b)
                total += 1
    out = []
    for keys in rooms:
        keys = sorted(keys)
        rng.shuffle(keys)
        out.append(keys)
    return {"rooms": out}
