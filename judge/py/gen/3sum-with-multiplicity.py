"""3Sum With Multiplicity at n = 3000 over values 0..100 (heavy repeats), so the count is huge
and a cubic scan does ~4.5 * 10^9 triples."""

SEEDS = 3


def generate(rng):
    hi = rng.choice([100, 10, 3])
    arr = [rng.randint(0, hi) for _ in range(3000)]
    target = rng.randint(0, min(300, 3 * hi))
    return {"arr": arr, "target": target}
