"""Maximum Beauty of an Array After Applying Operation at n = 2 * 10^4 values up to 10^5 with a
mid-sized k, so counting each window by a full scan is 4 * 10^8 steps."""

SEEDS = 2
N = 2 * 10**4
LIMIT = 10**5


def generate(rng):
    return {
        "nums": [rng.randint(0, LIMIT) for _ in range(N)],
        "k": rng.randint(LIMIT // 50, LIMIT // 10),
    }
