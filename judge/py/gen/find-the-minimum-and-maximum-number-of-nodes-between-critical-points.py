"""Critical Points on a 10^5-node list: a zigzag where almost every node is critical, random
values, or a monotone list with only two critical points."""

SEEDS = 3
N = 10**5


def generate(rng):
    shape = rng.randrange(3)
    if shape == 0:
        head = [rng.randint(1, 50) if i % 2 else rng.randint(51, 10**5) for i in range(N)]
    elif shape == 1:
        head = [rng.randint(1, 10) for _ in range(N)]
    else:
        head = sorted(rng.randint(1, 10**5) for _ in range(N))
        head[1] = 10**5
        head[-2] = 1
    return {"head": head}
