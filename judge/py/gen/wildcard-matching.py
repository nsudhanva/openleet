"""Wildcard Matching at 2000 x 2000: many stars between repeated letters with a mismatch at
the very end (exponential for naive backtracking), or a real match built from s."""

SEEDS = 3
N = 2000


def generate(rng):
    shape = rng.getrandbits(6) % 3  # seeds 0-2 land on three different shapes
    if shape == 0:
        s = "a" * N
        p = ("*a" * 999)[: N - 1] + "b"
        return {"s": s, "p": p}
    s = "".join(rng.choice("ab") for _ in range(N))
    # Build p from s: drop runs into '*', replace letters with '?', keep the rest.
    p, i = [], 0
    while i < N and len(p) < N - 2:
        r = rng.random()
        if r < 0.1:
            p.append("*")
            i += rng.randint(0, 5)
        elif r < 0.3:
            p.append("?")
            i += 1
        else:
            p.append(s[i])
            i += 1
    p.append("*")
    if shape == 2:
        p.append("c")  # nothing in s is 'c': a forced mismatch at the end
    return {"s": s, "p": "".join(p)[:N]}
