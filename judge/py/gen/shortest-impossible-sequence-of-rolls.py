"""Shortest Impossible Sequence of Rolls at n = 5 * 10^4 with k ~ 10^4: a few groups each holding
every face once plus repeats, so recounting the faces seen in the current group at every roll is
~n * k / 2 work."""

SEEDS = 2
N = 5 * 10**4
K = 10**4


def generate(rng):
    k = K + rng.randrange(K // 5)
    rolls = []
    while len(rolls) < N:
        group = list(range(1, k + 1)) + [rng.randint(1, k) for _ in range(k // 4)]
        rng.shuffle(group)
        rolls += group
    return {"rolls": rolls[:N], "k": k}
