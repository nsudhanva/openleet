"""X of a Kind at 10^4 cards: group counts sharing a gcd greater than 1 (true), or counts whose
gcd drops to 1 only through the last value."""

from _shapes import pick_shape

SEEDS = 3
N = 10**4


def generate(rng):
    shape = pick_shape(rng)
    g = rng.choice([2, 3, 6, 7])
    values = rng.sample(range(10**4), 2000)
    deck = []
    for v in values:
        k = g * rng.randint(1, 3)
        if len(deck) + k > N - 10:
            break
        deck.extend([v] * k)
    if shape == 1:
        taken = set(values)
        fresh = next(v for v in range(10**4) if v not in taken)
        deck.extend([fresh] * (g + 1))  # gcd(g, g + 1) = 1
    elif shape == 2:
        deck = [values[0]] * N  # one big group
    rng.shuffle(deck)
    return {"deck": deck}
