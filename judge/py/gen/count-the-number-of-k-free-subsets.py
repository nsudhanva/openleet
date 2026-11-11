"""Count the Number of K-Free Subsets at 50 distinct values forming a few long chains x, x + k,
x + 2k, ..., so listing the ~10^9 or more k-free subsets one by one is hopeless."""

SEEDS = 2
N = 50
LIMIT = 1000


def generate(rng):
    k = rng.randint(1, 15)
    nums = set()
    while len(nums) < N:
        x = rng.randint(1, LIMIT)
        for _ in range(rng.randint(5, 25)):
            if x > LIMIT or len(nums) == N:
                break
            nums.add(x)
            x += k
    nums = list(nums)
    rng.shuffle(nums)
    return {"nums": nums, "k": k}
