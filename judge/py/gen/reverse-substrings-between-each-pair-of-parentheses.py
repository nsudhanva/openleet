"""Reverse Parentheses at length 2000: ~500 levels of nesting with letters at every level (the
quadratic worst case for repeated reversal), or a random balanced string."""

SEEDS = 2
LETTERS = "abcdefghijklmnopqrstuvwxyz"


def generate(rng):
    if rng.random() < 0.5:
        depth = 499
        left = "".join(rng.choice(LETTERS) + "(" for _ in range(depth))
        right = "".join(")" + rng.choice(LETTERS) for _ in range(depth))
        core = "".join(rng.choice(LETTERS) for _ in range(2000 - 4 * depth))
        return {"s": left + core + right}
    out, open_count = [], 0
    while len(out) + open_count < 2000:
        room = 2000 - len(out) - open_count
        r = rng.random()
        if r < 0.3 and room >= 2:
            out.append("(")
            open_count += 1
        elif r < 0.55 and open_count:
            out.append(")")
            open_count -= 1
        else:
            out.append(rng.choice(LETTERS))
    out.extend(")" * open_count)
    return {"s": "".join(out)}
