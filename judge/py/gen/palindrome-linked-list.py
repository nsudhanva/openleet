"""Palindrome Linked List at 10^5 nodes: a true palindrome, or one broken in the very middle."""

SEEDS = 2
N = 10**5


def generate(rng):
    half = [rng.randint(0, 9) for _ in range(N // 2)]
    head = half + half[::-1]
    if rng.random() < 0.5:
        i = N // 2 - 1
        head[i] = (head[i] + 1) % 10
    return {"head": head}
