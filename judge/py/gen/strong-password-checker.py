"""Strong Password Checker at the maximum length of 50 with many repeating runs of varied
lengths, the hard case for the deletion/replacement interplay."""

SEEDS = 3
N = 50
POOLS = ["abcdefghijklmnopqrstuvwxyz", "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "0123456789", ".!"]


def generate(rng):
    n = rng.choice([N, N, rng.randint(21, N)])
    pools = rng.sample(POOLS, rng.randint(1, len(POOLS)))
    letters = "".join(pools)
    s = []
    while len(s) < n:
        c = rng.choice(letters)
        if s and s[-1] == c:
            continue
        s.extend([c] * min(n - len(s), rng.randint(1, 8)))
    return {"password": "".join(s)}
