"""Find Minimum in Rotated Sorted Array at n = 5000 distinct values, rotated by a random amount
(including a full rotation that leaves it sorted)."""

SEEDS = 3
N = 5000


def generate(rng):
    nums = sorted(rng.sample(range(-5000, 5001), N))
    k = rng.choice([N, 1, rng.randint(1, N)])
    return {"nums": nums[-k:] + nums[:-k] if k < N else nums}
