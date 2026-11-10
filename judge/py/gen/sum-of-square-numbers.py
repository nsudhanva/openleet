"""Sum of Square Numbers with c near 2^31 - 1, so an O(c) scan or a hash of all squares up to
c is punished; mixes true (built as a^2 + b^2) and arbitrary values."""

SEEDS = 3
LIMIT = 2**31 - 1


def generate(rng):
    shape = rng.getrandbits(6) % 3  # seeds 0-2 land on three different shapes
    if shape == 0:
        return {"c": LIMIT}
    if shape == 1:
        a = rng.randint(0, 46340)
        b = rng.randint(0, int((LIMIT - a * a) ** 0.5))
        while a * a + b * b > LIMIT:
            b -= 1
        return {"c": a * a + b * b}
    return {"c": rng.randint(LIMIT - 10**6, LIMIT)}
