"""Longest Happy Prefix at length 10^5: all one letter or a short repeated period (comparing
every prefix to its suffix is quadratic), or random letters."""

SEEDS = 3
N = 10**5


def generate(rng):
    shape = rng.choice(["same", "period", "random"])
    if shape == "same":
        s = "a" * N
    elif shape == "period":
        unit = "".join(rng.choice("ab") for _ in range(rng.randint(2, 50)))
        s = (unit * (N // len(unit) + 1))[: N - 1] + "z"
        if rng.random() < 0.5:
            s = (unit * (N // len(unit) + 1))[:N]
    else:
        s = "".join(rng.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(N))
    return {"s": s}
