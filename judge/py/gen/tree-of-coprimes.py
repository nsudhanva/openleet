"""Tree of Coprimes at n = 5 * 10^4: a deep thin tree of multiples of 6 with a rare power of 2 or
3, so walking up the ancestors of every node until a coprime one is ~10^9 steps; in one seed a few
nodes with values coprime to 6 sit in the middle of the tree, so the walk cannot be skipped by
noticing that no value in the tree is coprime to a node's."""

from _shapes import pick_shape

SEEDS = 3
N = 5 * 10**4
RARE = (2, 3, 4, 8, 9, 16, 27, 32)
COPRIME = (5, 7, 11, 13, 25, 35)


def generate(rng):
    shape = pick_shape(rng)
    label = rng.sample(range(N), N)
    edges = []
    for i in range(1, N):
        p = i - 1 if rng.random() < 0.9 else rng.randrange(max(0, i - 30), i)
        e = [label[p], label[i]]
        rng.shuffle(e)
        edges.append(e)
    rng.shuffle(edges)
    nums = [rng.choice(RARE) if rng.random() < 0.002 else 6 * rng.randint(1, 8) for _ in range(N)]
    if shape == 1:
        for _ in range(3):
            nums[label[rng.randrange(N // 4, 3 * N // 4)]] = rng.choice(COPRIME)
    return {"nums": nums, "edges": edges}
