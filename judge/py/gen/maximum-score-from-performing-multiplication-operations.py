"""Maximum Score from Performing Multiplication Operations at m = 300 and n = 10^5, so trying
both ends at every step without memoising makes 2^300 calls and a table over n is 10^10 cells."""

SEEDS = 2
N = 10**5
M = 300


def generate(rng):
    nums = [rng.randint(-1000, 1000) for _ in range(N)]
    return {"nums": nums, "multipliers": [rng.randint(-1000, 1000) for _ in range(M)]}
