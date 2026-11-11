"""Maximum Size Subarray Sum Equals k at n = 3 * 10^4: values drifting downward with one short
rising block making k, so checking every subarray (longest first) costs ~4.5 * 10^8 steps."""

SEEDS = 2
N = 3 * 10**4
BLOCK = 30


def generate(rng):
    nums = [rng.randint(-(10**4), 5000) for _ in range(N)]
    at = rng.randrange(N - BLOCK)
    nums[at : at + BLOCK] = [10**4] * BLOCK
    return {"nums": nums, "k": 10**4 * BLOCK}
