"""Is Subsequence with t of 10^4 letters and s of 100: s matched only near the end of t, or
failing on its last letter."""

SEEDS = 3


def generate(rng):
    t = ["a"] * 10**4
    for i in range(rng.randrange(9000, 9900), 10**4):
        t[i] = rng.choice("ab")
    s = [rng.choice("ab") for _ in range(100)]
    if rng.random() < 0.34:
        s[-1] = "c"
    elif rng.random() < 0.5:
        s = "".join(t[i] for i in sorted(rng.sample(range(10**4), 100)))
    return {"s": "".join(s), "t": "".join(t)}
