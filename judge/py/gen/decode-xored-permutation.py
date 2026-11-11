"""Decode XORed Permutation at n = 2^15 - 1 with perm[0] in the middle third: every wrong first
value then decodes to an in-range, duplicate-free prefix until it hits 0, so trying first values
in order costs ~2 * 10^8 steps."""

SEEDS = 2
N = 2**15 - 1


def generate(rng):
    perm = list(range(1, N + 1))
    rng.shuffle(perm)
    first = rng.randint(N // 3, 2 * N // 3)
    i = perm.index(first)
    perm[0], perm[i] = perm[i], perm[0]
    return {"encoded": [perm[i] ^ perm[i + 1] for i in range(N - 1)]}
