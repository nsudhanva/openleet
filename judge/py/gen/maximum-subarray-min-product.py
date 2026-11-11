"""Maximum Subarray Min-Product at n = 3 * 10^4 sorted values, ascending on one seed and
descending on the other, so extending every start, or expanding each element while its
neighbours are no smaller, costs ~4.5 * 10^8 steps."""

SEEDS = 2
N = 3 * 10**4


def generate(rng):
    # The first draw is 0.84 for seed 0 and 0.13 for seed 1, so the seeds take both directions.
    descending = rng.random() < 0.5
    nums = sorted((rng.randint(1, 10**7) for _ in range(N)), reverse=descending)
    return {"nums": nums}
