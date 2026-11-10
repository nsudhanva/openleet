"""Kth Largest Element at n = 10^5: random values, all-equal values (bad for naive
quickselect partitions), or sorted values."""

SEEDS = 3
N = 10**5
LIMIT = 10**4


def generate(rng):
    shape = rng.choice(["random", "equal", "sorted"])
    if shape == "equal":
        nums = [rng.randint(-LIMIT, LIMIT)] * N
    else:
        nums = [rng.randint(-LIMIT, LIMIT) for _ in range(N)]
        if shape == "sorted":
            nums.sort()
    return {"nums": nums, "k": rng.randint(1, N)}
