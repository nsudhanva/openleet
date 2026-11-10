"""Two Sum at n = 10^4 with the only valid pair placed last, so a quadratic scan does all
~5 * 10^7 comparisons."""

SEEDS = 2
N = 10**4
LIMIT = 10**9


def generate(rng):
    # Distinct values that leave no accidental second pair: all odd, target even and huge.
    values = rng.sample(range(-LIMIT // 2, LIMIT // 2), N - 2)
    values = [v * 2 + 1 for v in values]
    used = set(values)
    while True:
        a = rng.randrange(-LIMIT // 2, LIMIT // 2) * 2
        b = rng.randrange(-LIMIT // 2, LIMIT // 2) * 2
        if a != b and a not in used and b not in used:
            break
    # Odd + odd is even, so make the target odd-free: a and b are even, every other pair
    # sums to an even number too, so check sums against the target explicitly.
    target = a + b
    seen = set()
    for v in values:
        if target - v in seen:
            return generate(rng)
        seen.add(v)
    if target - a in used or target - b in used:
        return generate(rng)
    return {"nums": [*values, a, b], "target": target}
