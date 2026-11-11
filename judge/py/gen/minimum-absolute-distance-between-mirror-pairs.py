"""Minimum Absolute Distance Between Mirror Pairs at n = 8 * 10^4 with the only mirror pair at
the two ends, so checking every pair is 3 * 10^9 steps."""

SEEDS = 2
N = 8 * 10**4
LIMIT = 10**9


def reverse(x):
    return int(str(x)[::-1])


def generate(rng):
    while True:
        a = rng.randint(10, LIMIT)
        b = reverse(a)
        if a % 10 and a != b:
            break
    used = {a, b}
    middle = []
    while len(middle) < N - 2:
        x = rng.randint(1, LIMIT)
        if x in used:
            continue
        r = reverse(x)
        if r != x and r not in used:
            used.add(x)
            used.add(r)
            middle.append(x)
    return {"nums": [a, *middle, b]}
