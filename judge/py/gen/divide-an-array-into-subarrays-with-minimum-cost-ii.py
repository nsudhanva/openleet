"""Divide an Array Into Subarrays With Minimum Cost II at n = 10^5 with dist near n / 2 and k
near dist / 2, so sorting every window afresh is ~5 * 10^4 sorts of 5 * 10^4."""

SEEDS = 2
N = 10**5


def generate(rng):
    nums = [rng.randint(1, 10**8) for _ in range(N)]
    dist = rng.randint(N * 2 // 5, N // 2)
    k = rng.randint(max(3, dist // 3), dist * 2 // 3)
    return {"nums": nums, "k": k, "dist": dist}
