"""Two Sum at n = 10^4 with the only valid pair placed last, so a quadratic scan does all
~5 * 10^7 comparisons."""

SEEDS = 2
N = 10**4
LIMIT = 10**9


def generate(rng):
    # Distinct odd values plus an even pair (a, b): only the pair or two odd values can reach the
    # even target a + b, and the scan below rules out the odd pairs.
    values = rng.sample(range(-LIMIT // 2, LIMIT // 2), N - 2)
    values = [v * 2 + 1 for v in values]
    used = set(values)
    while True:
        a = rng.randrange(-LIMIT // 2, LIMIT // 2) * 2
        b = rng.randrange(-LIMIT // 2, LIMIT // 2) * 2
        if a != b and a not in used and b not in used:
            break
    target = a + b
    seen = set()
    for v in values:
        if target - v in seen:
            return generate(rng)
        seen.add(v)
    return {"nums": [*values, a, b], "target": target}
