"""3Sum Smaller at n = 1500 with values in [-100, 100] and a target near the middle, so a
cubic scan checks all ~5.6 * 10^8 triplets (the count stays under 10^9)."""

SEEDS = 2
N = 1500


def generate(rng):
    nums = [rng.randint(-100, 100) for _ in range(N)]
    return {"nums": nums, "target": rng.randint(-20, 20)}
