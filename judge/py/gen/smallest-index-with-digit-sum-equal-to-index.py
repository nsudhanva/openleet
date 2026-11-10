"""Smallest Index With Digit Sum Equal to Index on 100 values in [0, 1000], match late or never."""

SEEDS = 2


def generate(rng):
    def digit_sum(x):
        return sum(map(int, str(x)))

    nums = []
    for i in range(100):
        while True:
            v = rng.randint(0, 1000)
            if digit_sum(v) != i:
                break
        nums.append(v)
    if rng.random() < 0.5:
        nums[27] = 999  # digit sum 27, the largest reachable index
    return {"nums": nums}
