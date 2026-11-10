"""Find All Duplicates in an Array at n = 10^5, values in [1, n] each appearing once or twice:
about half duplicated, or a single duplicate."""

SEEDS = 2
N = 10**5


def generate(rng):
    dups = rng.choice([rng.randint(1, N // 2), 1])
    values = rng.sample(range(1, N + 1), N - dups)
    nums = values + values[:dups]
    rng.shuffle(nums)
    return {"nums": nums}
