"""Count The Repetitions with |s1| = |s2| = 100 and n1 = 10^6, so simulating every copy of s1
costs 10^8 steps; s2 is built from s1's letters so the answer is non-zero."""

SEEDS = 2
L = 100


def generate(rng):
    alphabet = rng.sample("abcdefghijklmnopqrstuvwxyz", rng.randint(2, 5))
    s1 = "".join(rng.choice(alphabet) for _ in range(L))
    s2 = "".join(rng.choice(alphabet) for _ in range(L))
    return {"s1": s1, "n1": 10**6, "s2": s2, "n2": rng.randint(1, 10**6)}
