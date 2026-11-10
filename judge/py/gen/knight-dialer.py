"""Knight Dialer at n near 5000, where naive recursion over 4,600-odd moves explodes."""

SEEDS = 2


def generate(rng):
    return {"n": rng.choice([5000, rng.randint(4000, 5000)])}
