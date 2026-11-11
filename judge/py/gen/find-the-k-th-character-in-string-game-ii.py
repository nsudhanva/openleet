"""Find the K-th Character in String Game II with k between 10^13 and 10^14 and up to 100
operations, so building the word up to k characters is out of reach."""

SEEDS = 2


def generate(rng):
    ops = [rng.randrange(2) for _ in range(rng.randint(47, 100))]
    return {"k": rng.randint(10**13, 10**14), "operations": ops}
