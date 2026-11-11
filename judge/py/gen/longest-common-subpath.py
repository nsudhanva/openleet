"""Longest Common Subpath with two paths of 5 * 10^4 cities each (the maximum total) sharing one
stretch of 2.4-3 * 10^4 cities, so comparing subpaths as tuples or byte strings in the binary
search costs ~10^10 steps."""

SEEDS = 2
N = 10**5
M = 2
LENGTH = 5 * 10**4
COMMON = 3 * 10**4


def walk(rng, length, prev=-1):
    out = []
    for _ in range(length):
        x = rng.randrange(N)
        while x == prev:
            x = rng.randrange(N)
        out.append(x)
        prev = x
    return out


def generate(rng):
    common = walk(rng, COMMON - rng.randrange(COMMON // 5 + 1))
    paths = []
    for _ in range(M):
        before = rng.randint(0, LENGTH - len(common))
        head = walk(rng, before)
        while head and (head[-1] == common[0] or (len(head) > 1 and head[-1] == head[-2])):
            head[-1] = rng.randrange(N)
        tail = walk(rng, LENGTH - len(common) - before, common[-1])
        paths.append(head + common + tail)
    return {"n": N, "paths": paths}
