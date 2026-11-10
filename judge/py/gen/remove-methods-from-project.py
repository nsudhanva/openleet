"""Remove Methods From Project at n = 10^5 with 2 * 10^5 unique invocations: a suspicious
chain reached from k, with or without an outside caller into it."""

import itertools

SEEDS = 2
N = 10**5
M = 2 * 10**5


def generate(rng):
    k = rng.randrange(N)
    others = [v for v in range(N) if v != k]
    rng.shuffle(others)
    size = rng.randint(N // 4, N // 2)
    sus = [k, *others[: size - 1]]
    rest = others[size - 1 :]
    pairs = set()
    for a, b in itertools.pairwise(sus):
        pairs.add((a, b))
    while len(pairs) < M - 1:
        if rng.random() < 0.5:
            a, b = rng.choice(sus), rng.choice(sus)
        else:
            a, b = rng.choice(rest), rng.choice(rest)
        if a != b:
            pairs.add((a, b))
    if rng.random() < 0.5:
        while True:
            a, b = rng.choice(rest), rng.choice(sus)
            if (a, b) not in pairs:
                pairs.add((a, b))
                break
    else:
        while True:
            a, b = rng.choice(sus), rng.choice(rest)
            if (a, b) not in pairs:
                pairs.add((a, b))
                break
    invocations = [list(p) for p in sorted(pairs)]
    rng.shuffle(invocations)
    return {"n": N, "k": k, "invocations": invocations}
