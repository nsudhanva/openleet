"""Jump Game IV at n = 5 * 10^4: one value repeated almost everywhere (the BFS must clear each
value's list after use), or a few values in long runs."""

SEEDS = 3
N = 5 * 10**4


def generate(rng):
    shape = rng.randrange(3)
    if shape == 0:
        arr = [7] * (N - 1) + [rng.randint(-(10**8), 10**8)]
    elif shape == 1:
        arr = [rng.choice([1, 2, 3]) for _ in range(N)]
    else:
        arr = [rng.randint(-(10**8), 10**8) for _ in range(N)]
        for i in range(0, N, 2):
            arr[i] = arr[i + 1] + 1 if arr[i + 1] < 10**8 else arr[i + 1] - 1
    return {"arr": arr}
