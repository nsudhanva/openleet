"""Decode Ways II at length 10^5: mostly '*', '1' and '2' so every position branches, or all
'*'."""

SEEDS = 2
N = 10**5


def generate(rng):
    s = "*" * N
    if rng.random() < 0.5:
        s = "".join(rng.choice("**12120123456789") for _ in range(N))
    return {"s": s}
