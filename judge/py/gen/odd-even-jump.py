"""Odd Even Jump at n = 2 * 10^4: random values, or a sorted-ish array with many duplicates so
a linear scan for each jump target is quadratic."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    if rng.random() < 0.5:
        arr = [rng.randrange(10**5) for _ in range(N)]
    else:
        arr = sorted(rng.randrange(1000) for _ in range(N))
        if rng.random() < 0.5:
            arr.reverse()
    return {"arr": arr}
