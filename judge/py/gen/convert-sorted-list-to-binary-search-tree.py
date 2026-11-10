"""Convert Sorted List to Binary Search Tree with 2^14 - 1 = 16383 nodes (near the 2 * 10^4
maximum): every sublist has odd length, so any middle choice builds the same tree."""

SEEDS = 2
N = 2**14 - 1


def generate(rng):
    if rng.random() < 0.5:
        head = sorted(rng.sample(range(-(10**5), 10**5 + 1), N))
    else:
        head = sorted(rng.randint(-(10**5), 10**5) for _ in range(N))
    return {"head": head}
