"""Remove All Occurrences at length 1000: copies of part nested inside each other, so every
removal exposes another and the string collapses in a long cascade."""

SEEDS = 2


def generate(rng):
    m = rng.choice([2, 3, 5])
    part = "".join(rng.choice("abc") for _ in range(m))
    s = part
    while len(s) + m <= 1000:
        if rng.random() < 0.8:
            i = rng.randint(0, len(s))
            s = s[:i] + part + s[i:]
        else:
            s = s + rng.choice("abc")
    return {"s": s, "part": part}
