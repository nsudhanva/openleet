"""Maximum Subsequence Score at n = 7 * 10^4 with k between n / 3 and 2n / 3, so fixing each
minimum and summing the k largest partners anew costs ~2.5 * 10^9 steps."""

SEEDS = 2
N = 7 * 10**4


def generate(rng):
    nums1 = [rng.randint(0, 10**5) for _ in range(N)]
    nums2 = [rng.randint(0, 10**5) for _ in range(N)]
    return {"nums1": nums1, "nums2": nums2, "k": rng.randint(N // 3, 2 * N // 3)}
