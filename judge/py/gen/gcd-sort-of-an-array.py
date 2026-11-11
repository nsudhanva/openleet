"""3 * 10^4 values below 10^5: multiples of 2, 3 and 5 (one component, bridged by 6 and 10)
shuffled around isolated primes above 5 * 10^4 that sit in their sorted places, two of them
swapped half the time, so testing every pair's gcd costs ~4.5 * 10^8 steps."""

from _shapes import primes_upto

SEEDS = 2
N = 3 * 10**4
LIMIT = 10**5


def generate(rng):
    swap = rng.getrandbits(1)
    lone = rng.sample([p for p in primes_upto(LIMIT) if p > LIMIT // 2], N // 10)
    factors = rng.choices((2, 3, 5), k=N - N // 10 - 2)
    linked = [6, 10] + [rng.randint(1, LIMIT // q) * q for q in factors]
    nums = sorted(lone + linked)
    # Shuffle the linked values among their own positions; the lone primes stay put.
    lone = set(lone)
    spots = [i for i, v in enumerate(nums) if v in lone]
    free = [i for i, v in enumerate(nums) if v not in lone]
    vals = [nums[i] for i in free]
    rng.shuffle(vals)
    for i, v in zip(free, vals, strict=True):
        nums[i] = v
    if swap:
        a, b = rng.sample(spots[-100:], 2)
        nums[a], nums[b] = nums[b], nums[a]
    return {"nums": nums}
