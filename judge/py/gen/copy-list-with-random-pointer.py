"""Copy List with Random Pointer at the maximum 1000 nodes: random pointers everywhere, or
every node pointing to the head or tail."""

SEEDS = 2
N = 1000


def generate(rng):
    shape = rng.random() < 0.5
    head = []
    for i in range(N):
        val = rng.randint(-(10**4), 10**4)
        if shape:
            rnd = None if rng.random() < 0.1 else rng.randrange(N)
        else:
            rnd = rng.choice([0, N - 1, i])
        head.append([val, rnd])
    return {"head": head}
