"""Check if DFS Strings Are Palindromes at n = 3 * 10^4: a chain through nine nodes in ten with
the rest hung on random nodes, on nearly all-'a' letters, so building and checking every node's
DFS string is quadratic."""

SEEDS = 2
N = 3 * 10**4


def generate(rng):
    label = list(range(1, N))
    rng.shuffle(label)
    label = [0, *label]
    parent, tip = [-1] * N, 0
    for i in range(1, N):
        if rng.random() < 0.9:
            parent[label[i]], tip = label[tip], i
        else:
            parent[label[i]] = label[rng.randrange(i)]
    rare = rng.choice("bcz")
    s = "".join(rare if rng.random() < 0.001 else "a" for _ in range(N))
    return {"parent": parent, "s": s}
