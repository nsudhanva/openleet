"""Jump Game V at the maximum n = 1000 with d up to n: a long descending staircase (longest
chain), random heights, or many equal heights that block jumps."""

SEEDS = 3
N = 1000


def generate(rng):
    shape = rng.randrange(3)
    if shape == 0:
        arr = list(range(10**5, 10**5 - N, -1))
    elif shape == 1:
        arr = [rng.randint(1, 10**5) for _ in range(N)]
    else:
        arr = [rng.randint(1, 5) for _ in range(N)]
    d = rng.choice([N, rng.randint(1, N), 1])
    return {"arr": arr, "d": d}
