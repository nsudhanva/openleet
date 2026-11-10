"""Jump Game II at n = 10^4 with values up to 1000 and the end always reachable: all ones (n - 1
jumps), or mostly ones with occasional long jumps."""

SEEDS = 3
N = 10**4


def generate(rng):
    shape = rng.randrange(3)
    if shape == 0:
        nums = [1] * N
    elif shape == 1:
        nums = [rng.randint(1, 1000) if rng.random() < 0.01 else 1 for _ in range(N)]
    else:
        nums = [rng.randint(1, 1000) for _ in range(N)]
    nums[-1] = rng.randint(0, 1000)
    return {"nums": nums}
