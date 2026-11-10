"""First Missing Positive at n = 10^5: a shuffled 1..n with one gap (or none), duplicates, and
large negatives and positives mixed in."""

SEEDS = 3
N = 10**5


def generate(rng):
    shape = rng.randrange(3)
    if shape == 0:
        nums = list(range(1, N + 1))
    elif shape == 1:
        nums = list(range(1, N + 1))
        nums[rng.randrange(N)] = rng.choice([-(2**31), 0, 2**31 - 1, 7])
    else:
        nums = [
            rng.randint(-(2**31), 2**31 - 1) if rng.random() < 0.3 else rng.randint(1, N)
            for _ in range(N)
        ]
    rng.shuffle(nums)
    return {"nums": nums}
