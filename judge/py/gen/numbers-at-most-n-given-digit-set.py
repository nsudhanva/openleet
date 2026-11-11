"""Numbers At Most N with eight or nine digits and n near 10^9, so listing every candidate
number is ~10^8 or more."""

SEEDS = 2
LOW, HIGH = 9 * 10**8, 10**9


def generate(rng):
    k = rng.choice((8, 9))
    digits = sorted(rng.sample("123456789", k))
    return {"digits": digits, "n": rng.randint(LOW, HIGH)}
