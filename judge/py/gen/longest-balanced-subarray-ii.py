"""Longest Balanced Subarray II at n = 3 * 10^4 of distinct values in a repeating odd, odd, even
pattern around one short alternating block, so balanced subarrays are short and extending every
start with a set costs ~4.5 * 10^8 steps."""

SEEDS = 2
N = 3 * 10**4


def generate(rng):
    # True marks an even. One alternating block sets the answer; every value is distinct, so
    # the distinct evens never run out before the array does.
    even = [i % 3 == 2 for i in range(N)]
    length = 2 * rng.randint(N // 300 + 1, N // 30 + 1)
    start = rng.randrange(N - length + 1)
    even[start : start + length] = [i % 2 == 1 for i in range(length)]
    evens = rng.sample(range(1, 5 * 10**4 + 1), sum(even))
    odds = rng.sample(range(5 * 10**4), N - len(evens))
    return {"nums": [2 * evens.pop() if e else 2 * odds.pop() + 1 for e in even]}
