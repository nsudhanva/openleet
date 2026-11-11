"""Concatenate Non-Zero Digits and Multiply by Sum II with a 2 * 10^4-digit string and 2 * 10^4
queries over long ranges, so rebuilding each substring's number costs ~2 * 10^8 digit steps."""

SEEDS = 2
M = 2 * 10**4
Q = 2 * 10**4


def generate(rng):
    zeros = rng.choice((0.1, 0.5))
    s = "".join("0" if rng.random() < zeros else str(rng.randint(1, 9)) for _ in range(M))
    queries = []
    for _ in range(Q):
        a, b = rng.randrange(M // 2), rng.randrange(M // 2, M)
        queries.append([a, b])
    return {"s": s, "queries": queries}
