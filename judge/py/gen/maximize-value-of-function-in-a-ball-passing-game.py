"""Maximize Value of Function in a Ball Passing Game at n = 5 * 10^4 and k near 10^10: a cycle of
a tenth to a fifth of the players fed by one long chain, so walking each start to the cycle is
~10^9 steps."""

SEEDS = 2
N = 5 * 10**4
K = 10**10


def generate(rng):
    labels = list(range(N))
    rng.shuffle(labels)
    cycle = rng.randint(N // 10, N // 5)
    receiver = [0] * N
    for i in range(cycle):
        receiver[labels[i]] = labels[(i + 1) % cycle]
    for i in range(cycle, N):
        # Nearly every player extends the one chain; rare short side branches.
        parent = i - 1 if rng.random() < 0.999 else rng.randrange(max(cycle, i - 50), i)
        receiver[labels[i]] = labels[parent]
    return {"receiver": receiver, "k": rng.randint(K - K // 10, K)}
