"""Count Paths That Can Form a Palindrome in a Tree at n = 2 * 10^4 nodes over 16 letters (random
or long and thin, ~10^4 distinct root masks), so walking the tree from every node, or pairing each
node with every distinct mask, costs 10^8+ steps."""

from _shapes import random_string

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    order = list(range(1, N))
    rng.shuffle(order)
    order = [0, *order]
    thin = rng.random() < 0.5
    parent = [-1] * N
    for t in range(1, N):
        p = t - 1 - min(t - 1, int(rng.expovariate(0.2))) if thin else rng.randrange(t)
        parent[order[t]] = order[p]
    return {"parent": parent, "s": random_string(rng, "abcdefghijklmnop", N)}
