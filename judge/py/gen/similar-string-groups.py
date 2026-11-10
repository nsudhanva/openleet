"""Similar String Groups with 300 anagrams of length 300: chains of single swaps (few large
groups) or random permutations, so the O(n^2 * L) pairwise check runs in full."""

from _shapes import pick_shape

SEEDS = 3


def generate(rng):
    shape = pick_shape(rng)
    L = 300
    base = [rng.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(L)]
    strs = []
    if shape == 0:
        cur = list(base)
        for _ in range(300):
            i, j = rng.sample(range(L), 2)
            cur[i], cur[j] = cur[j], cur[i]
            strs.append("".join(cur))
    elif shape == 1:
        for _ in range(300):
            cur = list(base)
            rng.shuffle(cur)
            strs.append("".join(cur))
    else:
        roots = []
        for _ in range(10):
            r = list(base)
            rng.shuffle(r)
            roots.append(r)
        for _ in range(300):
            cur = list(rng.choice(roots))
            i, j = rng.sample(range(L), 2)
            cur[i], cur[j] = cur[j], cur[i]
            strs.append("".join(cur))
    return {"strs": strs}
