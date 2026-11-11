"""Maximum Number of Occurrences of a Substring on 10^5 letters over "ab" with sizes near 20, so the
substrings are nearly all distinct and counting each one by a scan is quadratic."""

SEEDS = 2
N = 10**5


def generate(rng):
    s = "".join(rng.choice("ab") for _ in range(N))
    min_size = rng.randint(18, 22)
    return {"s": s, "maxLetters": 2, "minSize": min_size, "maxSize": min_size + rng.randint(0, 3)}
