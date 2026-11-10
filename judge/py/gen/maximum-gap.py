"""Maximum Gap at n = 10^5 with values up to 10^9: random values, clustered values with one
big hole, or all equal."""

SEEDS = 3
N = 10**5


def generate(rng):
    shape = rng.choice(["random", "hole", "equal"])
    if shape == "equal":
        nums = [rng.randint(0, 10**9)] * N
    elif shape == "hole":
        nums = [rng.randint(0, 10**6) for _ in range(N // 2)]
        nums += [rng.randint(10**9 - 10**6, 10**9) for _ in range(N - N // 2)]
        rng.shuffle(nums)
    else:
        nums = [rng.randint(0, 10**9) for _ in range(N)]
    return {"nums": nums}
