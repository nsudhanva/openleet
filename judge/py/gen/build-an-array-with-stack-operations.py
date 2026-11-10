"""Build an Array With Stack Operations at n = 100: a sparse strictly increasing target (many
push/pop pairs) or the full range."""

SEEDS = 2


def generate(rng):
    n = 100
    size = rng.choice([100, rng.randint(1, 20)])
    target = sorted(rng.sample(range(1, n + 1), size))
    return {"target": target, "n": n}
