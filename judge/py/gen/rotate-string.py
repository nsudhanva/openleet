"""Rotate String at length 100 over a two-letter alphabet: a true rotation, or a near-rotation
that differs in one character."""

from _shapes import pick_shape

SEEDS = 3


def generate(rng):
    shape = pick_shape(rng)
    s = "".join(rng.choice("ab") for _ in range(100))
    shift = rng.randrange(100)
    goal = list(s[shift:] + s[:shift])
    if shape == 1:
        i = rng.randrange(100)
        goal[i] = "b" if goal[i] == "a" else "a"
    elif shape == 2:
        goal = goal[:-1]
    return {"s": s, "goal": "".join(goal)}
