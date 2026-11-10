"""Maximum Binary Tree with 1000 unique values: sorted (a chain 1000 deep, quadratic for the
split-at-max recursion) or a random permutation."""

SEEDS = 2
N = 1000


def generate(rng):
    nums = rng.sample(range(1001), N)
    shape = rng.choice(["asc", "desc", "random"])
    if shape == "asc":
        nums.sort()
    elif shape == "desc":
        nums.sort(reverse=True)
    return {"nums": nums}
