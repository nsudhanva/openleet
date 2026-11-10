"""Chalkboard XOR Game at the maximum 1000 values below 2^16: random, or a last value chosen to
make the total XOR zero."""

SEEDS = 3


def generate(rng):
    n = rng.choice([1000, 999])
    nums = [rng.randint(0, 2**16 - 1) for _ in range(n)]
    if rng.random() < 0.5:
        x = 0
        for v in nums[:-1]:
            x ^= v
        nums[-1] = x
    return {"nums": nums}
