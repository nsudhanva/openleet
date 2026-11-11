"""Count Triplets with Even XOR Set Bits II with three arrays of 2 * 10^4 values up to 10^9, so
even a pairwise loop over a and b (counting c by parity) does 4 * 10^8 steps."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    return {k: [rng.randint(0, 10**9) for _ in range(N)] for k in "abc"}
