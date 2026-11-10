"""GCD of Strings with both strings near 1000 uppercase letters built from a common short block
(answer non-trivial), or with the last letter changed."""

SEEDS = 3


def generate(rng):
    base = "".join(rng.choice("AB") for _ in range(rng.choice([1, 6, 12])))
    a = base * (rng.randint(500, 1000) // len(base))
    b = base * (rng.randint(500, 1000) // len(base))
    if rng.random() < 0.34:
        b = b[:-1] + ("C" if b[-1] != "C" else "D")
    return {"str1": a, "str2": b}
