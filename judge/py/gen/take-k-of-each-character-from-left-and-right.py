"""Take K of Each Character From Left and Right at n = 2 * 10^4 with k near a third of each letter's
count, so trying every left cut and rescanning from the right is ~10^8 steps."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    s = "".join(rng.choice("abc") for _ in range(N))
    k = min(s.count(c) for c in "abc") * rng.randint(30, 45) // 100
    return {"s": s, "k": k}
