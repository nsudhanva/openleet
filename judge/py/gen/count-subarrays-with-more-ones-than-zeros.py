"""Count Subarrays With More Ones Than Zeros at n = 10^5 bits, 45% ones (the balance drifts down,
so prefix sums insert near the front of a sorted list), so recounting every subarray costs 5 *
10^9 steps."""

SEEDS = 2
N = 10**5
ONES = 0.45


def generate(rng):
    return {"nums": [int(rng.random() < ONES) for _ in range(N)]}
