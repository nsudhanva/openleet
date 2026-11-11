"""Minimize Deviation in Array at n = 10^4 values 2^e * (small odd), so ~2 * 10^5 halvings each
finding the maximum by a scan cost ~4 * 10^9 steps."""

SEEDS = 2
N = 10**4


def generate(rng):
    nums = []
    for _ in range(N):
        odd = rng.randrange(1, 100, 2)
        nums.append(odd << rng.randint(10, (10**9 // odd).bit_length() - 1))
    return {"nums": nums}
