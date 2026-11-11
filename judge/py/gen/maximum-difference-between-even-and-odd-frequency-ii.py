"""Maximum Difference Between Even and Odd Frequency II at length 10^4 over '0'-'4' with small k,
so counting every substring of length at least k is ~5 * 10^7 substrings."""

SEEDS = 2
N = 10**4


def generate(rng):
    # Skewed digit weights keep the frequencies apart.
    weights = [rng.randint(1, 10) for _ in range(5)]
    s = "".join(rng.choices("01234", weights, k=N))
    return {"s": s, "k": rng.randint(1, 10)}
