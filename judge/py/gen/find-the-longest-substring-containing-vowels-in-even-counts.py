"""Find the Longest Substring Containing Vowels in Even Counts at length 3 * 10^4: four vowels
walk the prefix parity through all 16 masks in Gray-code order, with doubled copies of the fifth
inside each stretch, so the answer is a few thousand and both every-substring and longest-first
scans are quadratic."""

SEEDS = 2
N = 3 * 10**4


def generate(rng):
    vowels = list("aeiou")
    rng.shuffle(vowels)
    walk, pair = vowels[:4], vowels[4]
    consonants = "bcdfghjklmnpqrstvwxyz"
    weights = [rng.uniform(0.5, 1.5) for _ in range(16)]
    total = sum(weights)
    runs = [int((N - 15) * w / total) for w in weights]
    runs[rng.randrange(16)] += N - 15 - sum(runs)
    s = []
    for g in range(16):
        if g:
            # Gray codes g ^ (g >> 1) and its predecessor differ in the lowest set bit of g.
            s.append(walk[(g & -g).bit_length() - 1])
        run = [rng.choice(consonants) for _ in range(runs[g])]
        # Disjoint doubled copies keep the fifth vowel's count even outside them, so the mask
        # between two copies appears in this stretch only.
        slots = rng.sample(range(len(run) // 2), min(rng.randint(1, 4), len(run) // 2))
        for j in slots:
            run[2 * j] = run[2 * j + 1] = pair
        s += run
    return {"s": "".join(s)}
