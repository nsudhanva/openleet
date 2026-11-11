"""Replace Non-Coprime Numbers in Array at n = 10^4: a coprime half, then a half that collapses
into one value, so rescanning from the start after every merge costs ~2.5 * 10^7 gcds."""

SEEDS = 2
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


def generate(rng):
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
