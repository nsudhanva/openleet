"""Minimum Insertions to Balance a Parentheses String at length 10^5: random brackets, or
'(' runs followed by odd-length ')' runs."""

SEEDS = 3
N = 10**5


def generate(rng):
    if rng.random() < 0.5:
        return {"s": "".join(rng.choice("()") for _ in range(N))}
    parts, size = [], 0
    while size < N:
        run = "(" * rng.randint(1, 50) + ")" * rng.randint(1, 101)
        parts.append(run)
        size += len(run)
    return {"s": "".join(parts)[:N]}
