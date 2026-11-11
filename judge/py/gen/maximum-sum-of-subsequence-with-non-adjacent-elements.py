"""Maximum Sum of Subsequence With Non-Adjacent Elements at n = q = 2 * 10^4, so rerunning the
house-robber scan after every update costs ~4 * 10^8 steps."""

SEEDS = 2
N = 2 * 10**4
Q = 2 * 10**4


def generate(rng):
    nums = [rng.randint(-(10**5), 10**5) for _ in range(N)]
    queries = [[rng.randrange(N), rng.randint(-(10**5), 10**5)] for _ in range(Q)]
    return {"nums": nums, "queries": queries}
