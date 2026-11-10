"""Linked List Components with n = 10^4 shuffled node values and a large nums subset, so
checking membership with a list scan is quadratic."""

SEEDS = 2
N = 10**4


def generate(rng):
    head = list(range(N))
    rng.shuffle(head)
    size = rng.randint(N // 2, N)
    return {"head": head, "nums": rng.sample(range(N), size)}
