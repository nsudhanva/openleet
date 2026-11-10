"""Card Flipping Game at n = 1000: many cards with equal front and back (ruling values out), so
the minimum good value is pushed up, or random values."""

SEEDS = 2
N = 1000


def generate(rng):
    if rng.random() < 0.5:
        fronts = [rng.randint(1, 2000) for _ in range(N)]
        backs = [rng.randint(1, 2000) for _ in range(N)]
    else:
        fronts, backs = [], []
        for i in range(N):
            if i < 700:
                v = i + 1
                fronts.append(v)
                backs.append(v)
            else:
                fronts.append(rng.randint(1, 800))
                backs.append(rng.randint(1, 2000))
        pairs = list(zip(fronts, backs, strict=True))
        rng.shuffle(pairs)
        fronts = [a for a, _ in pairs]
        backs = [b for _, b in pairs]
    return {"fronts": fronts, "backs": backs}
