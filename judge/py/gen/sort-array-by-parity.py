"""Sort Array By Parity on 5000 values in [0, 5000], odds first then evens or mixed."""

SEEDS = 2


def generate(rng):
    nums = [rng.randint(0, 5000) for _ in range(5000)]
    if rng.random() < 0.5:
        nums.sort(key=lambda x: x % 2 == 0)
    return {"nums": nums}
