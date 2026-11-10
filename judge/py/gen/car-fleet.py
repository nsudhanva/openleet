"""Car Fleet at n = 10^5 distinct positions: random speeds, cars farther back much faster (they
pile into few fleets), or nearer cars always faster (n fleets)."""

SEEDS = 3
N = 10**5


def generate(rng):
    target = rng.randint(N + 1, 10**6)
    position = rng.sample(range(target), N)
    shape = rng.choice(["random", "one", "none"])
    if shape == "random":
        speed = [rng.randint(1, 10**6) for _ in range(N)]
    else:
        order = sorted(range(N), key=lambda i: position[i])
        speed = [0] * N
        for rank, i in enumerate(order):  # rank 0 is farthest from the target
            speed[i] = (N - rank) * 10 if shape == "one" else rank + 1
    rng_order = list(range(N))
    rng.shuffle(rng_order)
    return {
        "target": target,
        "position": [position[i] for i in rng_order],
        "speed": [speed[i] for i in rng_order],
    }
