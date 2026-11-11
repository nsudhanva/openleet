"""Kth Smallest Amount With Single Denomination Combination with 8 or 9 pairwise-coprime coins
(lcm over 10^9) and k from 10^9 to 2 * 10^9, so listing the amounts one at a time takes k steps
and marking one period of the pattern needs over a gigabyte."""

SEEDS = 2
POOL = [7, 9, 11, 13, 16, 17, 19, 23, 25]
K_LOW = 10**9
K_HIGH = 2 * 10**9


def generate(rng):
    coins = rng.sample(POOL, rng.randint(8, 9))
    return {"coins": coins, "k": rng.randint(K_LOW, K_HIGH)}
