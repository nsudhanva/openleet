"""Maximum XOR of Two Numbers at n = 2 * 10^5 over [0, 2^31 - 1], where the pairwise scan is 2 *
10^10 steps: random values, or values sharing their top 11 bits so the trie goes deep."""

SEEDS = 2
N = 2 * 10**5


def generate(rng):
    if rng.random() < 0.5:
        nums = [rng.randint(0, 2**31 - 1) for _ in range(N)]
    else:
        high = rng.randint(0, 2**31 - 1) & ~(2**20 - 1)
        nums = [high | rng.randint(0, 2**20 - 1) for _ in range(N)]
    return {"nums": nums}
