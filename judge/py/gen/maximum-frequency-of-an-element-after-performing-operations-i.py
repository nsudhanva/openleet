"""Maximum Frequency of an Element After Performing Operations I at n = 2 * 10^4 values up to
10^5 with k a quarter to a half of the range, so each target's window holds half the array or more
and counting it by a scan is ~3 * 10^8 steps."""

SEEDS = 2
N = 2 * 10**4
LIMIT = 10**5


def generate(rng):
    nums = [rng.randint(1, LIMIT) for _ in range(N)]
    return {
        "nums": nums,
        "k": rng.randint(LIMIT // 4, LIMIT // 2),
        "numOperations": rng.randint(0, N),
    }
