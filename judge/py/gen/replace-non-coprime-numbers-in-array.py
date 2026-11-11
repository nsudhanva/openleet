"""Replace Non-Coprime Numbers in Array at n = 10^4 or 2 * 10^4 + 1. One seed has a coprime half
and a half that collapses into one value, so rescanning from the start after every merge costs
~2.5 * 10^7 gcds. The others alternate two coprime values and end with their product, which merges
the whole array from the end one pair at a time, so repeating a left-to-right pass until nothing
merges needs one pass per element (~10^8 gcds or more)."""

from _shapes import pick_shape

SEEDS = 3
N = 10**4
PRIMES = [
    2,
    3,
    5,
    7,
    11,
    13,
    17,
    19,
    23,
    29,
    31,
    37,
    41,
    43,
    47,
    53,
    59,
    61,
    67,
    71,
    73,
    79,
    83,
    89,
    97,
]


def alternating(rng):
    p, r = rng.sample(PRIMES, 2)
    u, v = p, r
    while u * p <= 300 and rng.random() < 0.5:
        u *= p
    while v * r <= 300 and rng.random() < 0.5:
        v *= r
    return [u, v] * N + [u * v]


def generate(rng):
    if pick_shape(rng) != 0:
        return {"nums": alternating(rng)}
    q = rng.choice(PRIMES)
    others = [p for p in PRIMES if p != q]
    nums = [rng.choice(others)]
    while len(nums) < N // 2:
        p = rng.choice(others)
        if p != nums[-1]:
            nums.append(p * rng.choice((1, 1, p)) if p < 50 else p)
    # Adjacent values are powers of different primes, so the first half has no merge.
    tail = (q, q * q) if rng.random() < 0.5 else (q,)
    nums += [rng.choice(tail) for _ in range(N - len(nums))]
    return {"nums": nums}
