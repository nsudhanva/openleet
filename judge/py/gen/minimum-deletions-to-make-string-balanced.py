"""Minimum Deletions to Make String Balanced at n = 10^5: blocks of 'a' and 'b' with drifting
odds, so trying every split point and counting both sides is ~10^10 character checks."""

SEEDS = 2
N = 10**5
BLOCK = 2000


def generate(rng):
    out = []
    while len(out) < N:
        p = rng.random()
        out += ["b" if rng.random() < p else "a" for _ in range(rng.randint(1, BLOCK))]
    return {"s": "".join(out[:N])}
