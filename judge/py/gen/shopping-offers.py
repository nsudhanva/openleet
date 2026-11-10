"""Shopping Offers with 6 items, needs up to 10 each (11^6 states) and 100 small offers, so
search without memoization blows up."""

SEEDS = 3


def generate(rng):
    n = 6
    price = [rng.randint(0, 10) for _ in range(n)]
    needs = [10] * n if rng.random() < 0.5 else [rng.randint(5, 10) for _ in range(n)]
    special = []
    for _ in range(100):
        counts = [rng.choice([0, 0, 1, 1, 2, 3]) for _ in range(n)]
        if not any(counts):
            counts[rng.randrange(n)] = 1
        if rng.random() < 0.1:
            counts[rng.randrange(n)] = rng.randint(11, 50)  # unusable offer
        cost = sum(c * p for c, p in zip(counts, price, strict=True))
        special.append([*counts, max(0, min(50, cost - rng.randint(0, 5)))])
    return {"price": price, "special": special, "needs": needs}
