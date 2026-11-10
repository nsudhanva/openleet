"""Minimum Add to Make Parentheses Valid at the maximum length 1000: random brackets or a
run of ')' then '('."""

SEEDS = 3


def generate(rng):
    if rng.random() < 0.5:
        return {"s": "".join(rng.choice("()") for _ in range(1000))}
    cut = rng.randint(0, 1000)
    return {"s": ")" * cut + "(" * (1000 - cut)}
