"""Maximum Area of a Piece of Cake After Horizontal and Vertical Cuts with 8 * 10^4 distinct
unsorted cuts each way on a cake up to a quarter wider than the cut count, so inserting each cut
into a sorted list is ~3 * 10^9 element moves and comparing every pair of pieces far more."""

SEEDS = 2
N = 8 * 10**4


def generate(rng):
    h, w = rng.randint(N + 2, N + 2 + N // 4), rng.randint(N + 2, N + 2 + N // 4)
    return {
        "h": h,
        "w": w,
        "horizontalCuts": rng.sample(range(1, h), N),
        "verticalCuts": rng.sample(range(1, w), N),
    }
