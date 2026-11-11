"""Smallest Missing Non-negative Integer After Operations at n = 2 * 10^4 with every residue mod
value present (once each, or twice with value = n / 2), so the answer is ~n and searching the
list for each next residue is O(n^2)."""

SEEDS = 2
N = 2 * 10**4
LIMIT = 10**9


def generate(rng):
    value = N if rng.random() < 0.5 else N // 2
    residues = [i % value for i in range(N)]
    rng.shuffle(residues)
    hole = rng.randrange(N - 50, N)
    residues = [r for r in residues if r != hole % value or rng.random() < 0.5]
    while len(residues) < N:
        residues.append(rng.randrange(value))
    nums = []
    for r in residues:
        t = rng.randint(-((LIMIT + r) // value), (LIMIT - r) // value)
        nums.append(r + t * value)
    return {"nums": nums, "value": value}
