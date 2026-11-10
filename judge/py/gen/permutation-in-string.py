"""Permutation in String with |s2| = 10^4 over two letters: a long s1 whose permutation appears
only at the very end (or nowhere), punishing per-window sorting."""

SEEDS = 2
N = 10**4


def generate(rng):
    m = rng.randint(1000, 5000)
    s1 = "".join(rng.choice("ab") for _ in range(m))
    a = s1.count("a")
    s2 = "".join("a" if rng.random() < 0.3 else "b" for _ in range(N - m))
    if rng.random() < 0.5:
        tail = list(s1)
        rng.shuffle(tail)
    else:
        # Same length, one letter off, so no window ever matches the counts.
        tail = ["a"] * (a + 1) + ["b"] * (m - a - 1) if a < m else ["b"] + ["a"] * (m - 1)
    s2 = s2 + "".join(tail)
    return {"s1": s1, "s2": s2}
