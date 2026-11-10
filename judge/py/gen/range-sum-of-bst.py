"""Range Sum of BST with 2 * 10^4 unique values: a random BST, or a nearly linear one 20,000
levels deep; the range covers a middle slice."""

import itertools

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    vals = rng.sample(range(1, 10**5 + 1), N)
    left, right = [-1] * N, [-1] * N
    if rng.random() < 0.5:
        root = 0
        for i in range(1, N):
            cur = root
            while True:
                side = left if vals[i] < vals[cur] else right
                if side[cur] == -1:
                    side[cur] = i
                    break
                cur = side[cur]
    else:
        # A zigzag chain: alternate taking the smallest and largest remaining value.
        order = sorted(range(N), key=lambda i: vals[i])
        lo, hi, chain = 0, N - 1, []
        while lo <= hi:
            chain.append(order[lo])
            lo += 1
            if lo <= hi:
                chain.append(order[hi])
                hi -= 1
        root = chain[0]
        for a, b in itertools.pairwise(chain):
            (left if vals[b] < vals[a] else right)[a] = b
    out, queue, head = [], [root], 0
    while head < len(queue):
        v = queue[head]
        head += 1
        if v == -1:
            out.append(None)
            continue
        out.append(vals[v])
        queue.append(left[v])
        queue.append(right[v])
    while out and out[-1] is None:
        out.pop()
    low = rng.randint(1, 4 * 10**4)
    return {"root": out, "low": low, "high": rng.randint(low, 10**5)}
