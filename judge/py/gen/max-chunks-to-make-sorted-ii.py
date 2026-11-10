"""Max Chunks To Make Sorted II at n = 2000: strictly decreasing (one chunk), many duplicates,
or nearly sorted with local swaps."""

SEEDS = 3
N = 2000


def generate(rng):
    shape = rng.choice(["desc", "dups", "nearly"])
    if shape == "desc":
        arr = sorted(rng.sample(range(10**8 + 1), N), reverse=True)
    elif shape == "dups":
        arr = [rng.randint(0, 5) for _ in range(N)]
    else:
        arr = sorted(rng.randint(0, 10**8) for _ in range(N))
        for _ in range(100):
            i = rng.randrange(N - 1)
            arr[i], arr[i + 1] = arr[i + 1], arr[i]
    return {"arr": arr}
