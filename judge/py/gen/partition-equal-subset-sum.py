"""Partition Equal Subset Sum at n = 200, values up to 100: multiples of an odd prime p plus one
value that is not, with an even total, so the half-sum is unreachable mod p (no split, though
the gcd is 1) and the full O(n * sum) DP runs."""

SEEDS = 2
N = 200


def generate(rng):
    p = rng.choice((3, 5, 7))
    nums = [p * rng.randint(1, 100 // p) for _ in range(N - 1)]
    nums.append(rng.choice([v for v in range(1, 101) if v % p]))
    if sum(nums) % 2:
        # Moving one multiple by p flips the parity of the total.
        nums[0] += p if nums[0] + p <= 100 else -p
    rng.shuffle(nums)
    return {"nums": nums}
