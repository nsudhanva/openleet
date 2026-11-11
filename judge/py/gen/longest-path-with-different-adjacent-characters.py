"""Longest Path With Different Adjacent Characters on a deep random tree of 10^4 nodes (each
parent a node or two above) where every child's letter differs from its parent's, so searching
from every node costs ~10^8 steps."""

SEEDS = 2
N = 10**4


def generate(rng):
    letters = "abcdefghijklmnopqrstuvwxyz"
    parent = [-1] + [max(0, i - 1 - int(rng.expovariate(1.0))) for i in range(1, N)]
    s = [rng.choice(letters)]
    for i in range(1, N):
        c = rng.choice(letters)
        while c == s[parent[i]]:
            c = rng.choice(letters)
        s.append(c)
    return {"parent": parent, "s": "".join(s)}
