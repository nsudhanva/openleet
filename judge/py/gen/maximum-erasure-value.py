"""Maximum Erasure Value at n = 10^5 with values up to 10^4: long unique windows (a permutation
repeated), or few distinct values (many shrinks)."""

SEEDS = 2
N = 10**5


def generate(rng):
    if rng.random() < 0.5:
        perm = list(range(1, 10**4 + 1))
        nums = []
        while len(nums) < N:
            rng.shuffle(perm)
            nums.extend(perm)
        nums = nums[:N]
    else:
        nums = [rng.randint(1, 50) for _ in range(N)]
    return {"nums": nums}
