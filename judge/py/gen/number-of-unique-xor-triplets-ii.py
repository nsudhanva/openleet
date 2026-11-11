"""Number of Unique XOR Triplets II at the maximum 1,500 values, so trying every triplet costs
~5.6 * 10^8 steps."""

SEEDS = 2
N = 1500


def generate(rng):
    if rng.random() < 0.5:
        nums = rng.sample(range(1, N + 1), N)
    else:
        nums = [rng.randint(1, N) for _ in range(N)]
    return {"nums": nums}
