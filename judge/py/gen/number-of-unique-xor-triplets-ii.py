"""Number of Unique XOR Triplets II with the 750 even (or the 750 odd) values up to 1,500, each
once and shuffled. Every triplet XOR keeps the parity, so the result never fills the 2048 values
below the next power of two and a cubic search cannot stop early: ~7 * 10^7 triplets against
~10^6 pair XORs for the reference."""

SEEDS = 2
N = 1500


def generate(rng):
    nums = list(range(rng.randint(1, 2), N + 1, 2))
    rng.shuffle(nums)
    return {"nums": nums}
