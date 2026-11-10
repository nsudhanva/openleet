"""Partition Labels at length 500: many small partitions, or letters whose last occurrences
chain into one giant partition."""

SEEDS = 2
N = 500
LETTERS = "abcdefghijklmnopqrstuvwxyz"


def generate(rng):
    if rng.random() < 0.5:
        s = []
        while len(s) < N:
            block = rng.sample(LETTERS, rng.randint(1, 3))
            s.extend(rng.choice(block) for _ in range(rng.randint(1, 10)))
        s = s[:N]
    else:
        s = [rng.choice(LETTERS) for _ in range(N)]
    return {"s": "".join(s)}
