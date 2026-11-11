"""Make the XOR of All Segments Equal to Zero at n = 1000, k in [500, 1000]: each residue class
holds one or two values, so the DP over the values present is ~10^6 steps while trying all
2^10 values per class is ~k * 2^20 >= 5 * 10^8."""

SEEDS = 2
N = 1000
K = (500, 1000)
BITS = 10


def generate(rng):
    nums = [rng.randrange(1 << BITS) for _ in range(N)]
    return {"nums": nums, "k": rng.randint(*K)}
