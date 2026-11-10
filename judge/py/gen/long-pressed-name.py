"""Long Pressed Name with 1000-character typed strings stretched from a long name, sometimes
with one wrong character near the end."""

SEEDS = 3
LETTERS = "abcdefghijklmnopqrstuvwxyz"


def generate(rng):
    name = [rng.choice(LETTERS[:3]) for _ in range(rng.randint(400, 500))]
    typed = []
    budget = 1000 - len(name)
    for ch in name:
        extra = 0
        if budget > 0 and rng.random() < 0.6:
            extra = rng.randint(0, min(budget, 3))
            budget -= extra
        typed.extend([ch] * (1 + extra))
    if rng.random() < 0.5:
        pos = rng.randrange(len(typed) - 20, len(typed))
        typed[pos] = rng.choice([c for c in LETTERS if c != typed[pos]])
    return {"name": "".join(name), "typed": "".join(typed)}
