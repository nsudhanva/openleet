"""Partition Array into Three Parts at the maximum 5 * 10^4 values with no valid split: the
first part's sum s recurs as a prefix sum at every other index but 2s never does, so trying
every pair of cut points does ~6 * 10^8 checks."""

SEEDS = 2
N = 5 * 10**4
LIMIT = 10**4


def generate(rng):
    # arr = [x, zero-sum pairs (a, -a) with |a| != x, 2x]: the prefix sums are x and x +- a,
    # never 2x before the end, and the total is 3x.
    x = rng.randint(1, LIMIT // 2)
    arr = [x]
    while len(arr) < N - 1:
        a = rng.randint(1, LIMIT)
        if a == x:
            continue
        arr += [a, -a] if rng.random() < 0.5 else [-a, a]
    arr.append(2 * x)
    return {"arr": arr}
