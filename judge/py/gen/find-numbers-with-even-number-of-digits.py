"""Find Numbers with Even Number of Digits at n = 500 with digit counts mixed from 1 to 6."""

SEEDS = 2


def generate(rng):
    nums = []
    for _ in range(500):
        d = rng.randint(1, 6)
        nums.append(10**5 if d == 6 else rng.randint(10 ** (d - 1), 10**d - 1))
    return {"nums": nums}
