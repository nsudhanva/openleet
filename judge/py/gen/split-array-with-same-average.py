"""Split Array With Same Average at the maximum n = 30 (2^30 subsets): random values, values
that can never balance, or a constructed true case."""

SEEDS = 3


def generate(rng):
    shape = rng.getrandbits(6) % 3
    n = 30
    if shape == 0:
        nums = [rng.randint(0, 10**4) for _ in range(n)]
    elif shape == 1:
        # Equal values except one: the only balancing subsets do not exist.
        nums = [rng.randint(0, 10**4)] * (n - 1)
        nums.append(nums[0] + rng.choice([1, -1]) if nums[0] else 1)
        rng.shuffle(nums)
    else:
        # Two halves of 15 with the same sum (b is a with mass moved between entries).
        a = [rng.randint(0, 10**4) for _ in range(15)]
        b = list(a)
        for _ in range(10):
            i, j = rng.sample(range(15), 2)
            t = rng.randint(0, min(b[i], 10**4 - b[j]))
            b[i] -= t
            b[j] += t
        nums = a + b
        rng.shuffle(nums)
    return {"nums": nums}
