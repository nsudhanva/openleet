"""Stone Game IX at n = 10^4 with the residues mod 3 near-balanced, so a game search over how
many stones of each residue remain is ~10^10 states."""

SEEDS = 2
N = 10**4
LIMIT = 10**4


def generate(rng):
    zeros = rng.randint(N // 4, N // 3)
    ones = rng.randint((N - zeros) // 2 - 3, (N - zeros) // 2 + 3)
    stones = [3 * rng.randint(1, LIMIT // 3) for _ in range(zeros)]
    stones += [3 * rng.randint(0, LIMIT // 3 - 1) + 1 for _ in range(ones)]
    stones += [3 * rng.randint(0, LIMIT // 3 - 1) + 2 for _ in range(N - zeros - ones)]
    rng.shuffle(stones)
    return {"stones": stones}
