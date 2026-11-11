"""Jump Game VI at n = 25,000 with k about n / 2 and nums negative and non-increasing, so the
window's best score is always its oldest index and expires every step: taking or rescanning
the best of the last k scores costs ~3 * 10^8 comparisons even at C speed."""

SEEDS = 2
N = 25000


def generate(rng):
    nums = sorted((rng.randint(-(10**4), -1) for _ in range(N)), reverse=True)
    return {"nums": nums, "k": rng.randint(N * 2 // 5, N * 3 // 5)}
