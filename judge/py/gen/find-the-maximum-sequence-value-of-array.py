"""Find the Maximum Sequence Value of Array at n = 400 with k = 10 and full 7-bit values, so
redoing the OR-set DP at every split is ~n^2 k 2^7 against the single pass's ~n k 2^7."""

SEEDS = 2
N = 400
K = 10


def generate(rng):
    return {"nums": [rng.randint(1, 127) for _ in range(N)], "k": K}
