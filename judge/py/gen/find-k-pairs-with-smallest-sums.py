"""K Smallest Pairs with arrays of up to 10^5 and k = 10^4; one array holds distinct multiples of
10^4 and the other distinct values below 10^4, so every pair sum is unique."""

SEEDS = 2
B = 10**4


def generate(rng):
    big = sorted(i * B - 5 * 10**8 for i in rng.sample(range(10**5), 10**5))
    small = sorted(rng.sample(range(B), rng.randint(2000, B)))
    nums1, nums2 = (big, small) if rng.random() < 0.5 else (small, big)
    return {"nums1": nums1, "nums2": nums2, "k": 10**4}
