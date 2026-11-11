"""Find the Maximum Length of Valid Subsequence II at n = 1000 with k = 200, so running the
O(n^2) DP once per residue is ~10^8 steps against O(n^2) or O(n k) once."""

SEEDS = 2
N = 1000
K = 200


def generate(rng):
    spread = rng.choice((K, 10**7))
    return {"nums": [rng.randint(1, spread) for _ in range(N)], "k": K}
