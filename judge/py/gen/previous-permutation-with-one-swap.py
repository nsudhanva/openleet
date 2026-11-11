"""Previous Permutation With One Swap at the maximum 10^4 values: non-decreasing after the first
few, so the only descent is at the front and scanning the suffix of each index for a smaller
value does ~5 * 10^7 comparisons."""

SEEDS = 2
N = 10**4


def generate(rng):
    head = [rng.randint(N // 2, N) for _ in range(rng.randint(1, 3))]
    tail = sorted(rng.randint(1, N) for _ in range(N - len(head)))
    return {"arr": head + tail}
