"""A 100 x 100 matrix reshaped to a legal r x c (r * c = 10^4), or to an illegal size."""

SEEDS = 3


def generate(rng):
    mat = [[rng.randint(-1000, 1000) for _ in range(100)] for _ in range(100)]
    legal = [(r, 10**4 // r) for r in range(1, 301) if 10**4 % r == 0 and 10**4 // r <= 300]
    if rng.random() < 0.75:
        r, c = rng.choice(legal)
    else:
        while True:
            r, c = rng.randint(1, 300), rng.randint(1, 300)
            if r * c != 10**4:
                break
    return {"mat": mat, "r": r, "c": c}
