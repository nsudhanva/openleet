"""Maximum of Absolute Value Expression with 10^4 random pairs, so trying every pair of indices
is quadratic."""

SEEDS = 2
N = 10**4


def generate(rng):
    arr1 = [rng.randint(-(10**6), 10**6) for _ in range(N)]
    arr2 = [rng.randint(-(10**6), 10**6) for _ in range(N)]
    return {"arr1": arr1, "arr2": arr2}
