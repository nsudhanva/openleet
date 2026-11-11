"""Count Subarrays With More Ones Than Zeros at n = 10^5 bits, 10% ones (the balance drifts
down, so prefix sums insert near the front of a sorted list and bisect.insort moves ~10^5 items
per bit: 2.5 s a seed against 0.1 s for the reference). Recounting every subarray costs 5 * 10^9
steps."""

SEEDS = 6
N = 10**5
ONES = 0.1


def generate(rng):
    return {"nums": [int(rng.random() < ONES) for _ in range(N)]}
