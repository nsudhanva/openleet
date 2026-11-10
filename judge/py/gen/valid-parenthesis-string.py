"""Valid Parenthesis String at the maximum length 100, heavy with '*' so trying all three
meanings of each star is exponential."""

from _shapes import pick_shape

SEEDS = 3
N = 100


def generate(rng):
    shape = pick_shape(rng)
    if shape == 0:
        s = [rng.choice("(*") for _ in range(N // 2)] + [rng.choice(")*") for _ in range(N // 2)]
    elif shape == 1:
        s = ["*"] * N
        for i in rng.sample(range(N), 10):
            s[i] = rng.choice("()")
    else:
        s = [rng.choice("()*") for _ in range(N)]
    return {"s": "".join(s)}
