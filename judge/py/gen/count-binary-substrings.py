"""Count Binary Substrings at length 10^5: random bits, or a few huge runs where expanding
around every boundary is quadratic."""

SEEDS = 2
N = 10**5


def generate(rng):
    if rng.random() < 0.5:
        s = "".join(rng.choice("01") for _ in range(N))
    else:
        parts, total, bit = [], 0, rng.randint(0, 1)
        while total < N:
            run = min(rng.randint(10**4, 5 * 10**4), N - total)
            parts.append(str(bit) * run)
            total += run
            bit ^= 1
        s = "".join(parts)
    return {"s": s}
