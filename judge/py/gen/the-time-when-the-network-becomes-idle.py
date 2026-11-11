"""The Time When the Network Becomes Idle at n = 2 * 10^4: a long path out of the master with short
branches and patience 1 to 3, so replaying every resend of every server is ~10^8 steps."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    label = [0, *rng.sample(range(1, N), N - 1)]
    spine = N * 3 // 4
    edges = [[label[i - 1], label[i]] for i in range(1, spine)]
    edges += [[label[rng.randrange(i)], label[i]] for i in range(spine, N)]
    for e in edges:
        rng.shuffle(e)
    rng.shuffle(edges)
    return {"edges": edges, "patience": [0] + [rng.randint(1, 3) for _ in range(N - 1)]}
