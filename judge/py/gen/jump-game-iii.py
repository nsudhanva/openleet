"""Jump Game III at n = 5 * 10^4: a long chain of jumps that reaches the only zero last, or a
large reachable region with no zero in it."""

import itertools

SEEDS = 3
N = 5 * 10**4


def generate(rng):
    shape = rng.randrange(3)
    if shape == 0:
        # Visit a random permutation in order: each index jumps to the next one.
        order = list(range(N))
        rng.shuffle(order)
        arr = [0] * N
        for a, b in itertools.pairwise(order):
            arr[a] = abs(b - a)
        arr[order[-1]] = 0
        # Extra zeros elsewhere would shortcut; the forward jump from each node is the chain one.
        start = order[0]
        return {"arr": arr, "start": start}
    if shape == 1:
        arr = [rng.randint(1, N - 1) for _ in range(N)]
        return {"arr": arr, "start": rng.randrange(N)}
    arr = [1] * N
    arr[rng.choice([0, N - 1])] = 0
    return {"arr": arr, "start": N // 2}
