"""Maximum Number of Jumps to Reach the Last Index with n = 500 and a target that allows most but
not all jumps, so following every jump sequence without memoising cannot finish."""

SEEDS = 2
N = 500


def generate(rng):
    nums = [rng.randint(-1000, 1000) for _ in range(N)]
    return {"nums": nums, "target": rng.randint(900, 1300)}
