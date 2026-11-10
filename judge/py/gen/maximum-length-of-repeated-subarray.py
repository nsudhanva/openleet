"""Maximum Length of Repeated Subarray with both arrays at 1000: values from {0, 1} (many
partial matches), or a long shared block planted in random arrays."""

SEEDS = 2
N = 1000


def generate(rng):
    if rng.random() < 0.5:
        nums1 = [rng.randint(0, 1) for _ in range(N)]
        nums2 = [rng.randint(0, 1) for _ in range(N)]
    else:
        nums1 = [rng.randint(0, 100) for _ in range(N)]
        nums2 = [rng.randint(0, 100) for _ in range(N)]
        length = rng.randint(300, 700)
        a, b = rng.randint(0, N - length), rng.randint(0, N - length)
        nums2[b : b + length] = nums1[a : a + length]
    return {"nums1": nums1, "nums2": nums2}
