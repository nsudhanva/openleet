"""Binary Trees With Factors at the maximum 1000 distinct values drawn from 7-smooth numbers,
so almost every value has many factor pairs in the set and the count needs the modulus."""

SEEDS = 2


def generate(rng):
    smooth = [1]
    for p in (2, 3, 5, 7):
        smooth = [v * p**e for v in smooth for e in range(31) if v * p**e <= 10**9]
    smooth = sorted(v for v in smooth if v >= 2)
    # The 1000 smallest have the densest factor structure.
    arr = smooth[:1000] if rng.random() < 0.5 else rng.sample(smooth, 1000)
    rng.shuffle(arr)
    return {"arr": arr}
