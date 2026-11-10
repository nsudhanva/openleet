"""Find the Town Judge with n = 1000 and 10^4 unique trust pairs: a real judge trusted by all, or
a near-judge missing one truster or trusting someone back."""

SEEDS = 3
N = 1000
M = 10**4


def generate(rng):
    judge = rng.randint(1, N)
    pairs = {(a, judge) for a in range(1, N + 1) if a != judge}
    shape = rng.randrange(3)
    if shape == 1:
        pairs.discard((rng.choice([a for a in range(1, N + 1) if a != judge]), judge))
    elif shape == 2:
        other = judge % N + 1
        pairs.add((judge, other))
    while len(pairs) < M:
        a, b = rng.randint(1, N), rng.randint(1, N)
        if a != b and a != judge and b != judge:
            pairs.add((a, b))
    trust = [list(p) for p in sorted(pairs)]
    rng.shuffle(trust)
    return {"n": N, "trust": trust}
