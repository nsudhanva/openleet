"""Find the Divisibility Array of a String at length 10^5, the maximum, so taking each
prefix mod m from scratch, or keeping it as a growing big integer, is quadratic."""

SEEDS = 2
N = 10**5


def generate(rng):
    m = rng.choice((rng.randint(1, 50), rng.randint(1, 10**9)))
    return {"word": "".join(rng.choice("0123456789") for _ in range(N)), "m": m}
