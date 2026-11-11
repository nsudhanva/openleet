"""Sort Array by Moving Items to Empty Space at n = 10^5: a random permutation, so simulating
the moves and searching for each item's position costs ~n^2 steps."""

SEEDS = 2
N = 10**5


def generate(rng):
    nums = list(range(N))
    rng.shuffle(nums)
    return {"nums": nums}
