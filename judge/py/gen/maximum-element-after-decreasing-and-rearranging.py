"""Maximum Element After Decreasing and Rearranging at n = 10^5: huge random values (answer
n), or many small duplicates."""

SEEDS = 2
N = 10**5


def generate(rng):
    if rng.random() < 0.5:
        arr = [rng.randint(1, 10**9) for _ in range(N)]
    else:
        arr = [rng.randint(1, 1000) for _ in range(N)]
    return {"arr": arr}
