"""Total Characters in String After Transformations I at 1000 letters and t of 5000 to 10^4: the
string doubles about every 26 steps, so building it step by step blows up long before t."""

SEEDS = 2
N = 1000


def generate(rng):
    s = "".join(rng.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(N))
    return {"s": s, "t": rng.randint(5000, 10**4)}
