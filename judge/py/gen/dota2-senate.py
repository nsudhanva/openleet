"""Dota2 Senate at n = 10^4: random parties, or long blocks of each party so the voting runs
many rounds and naive removal from the middle is quadratic."""

SEEDS = 2
N = 10**4


def generate(rng):
    if rng.random() < 0.5:
        senate = "".join(rng.choice("RD") for _ in range(N))
    else:
        r = N // 2 + rng.randint(-3, 3)
        senate = "R" * r + "D" * (N - r)
        if rng.random() < 0.5:
            senate = senate[::-1]
    return {"senate": senate}
