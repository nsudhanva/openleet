"""Count Subarrays With Score Less Than K at n = 2 * 10^4 with k admitting windows of about a
third of the array, so extending each start until the score fails costs ~10^8 steps."""

SEEDS = 2
N = 2 * 10**4
LIMIT = 10**5


def generate(rng):
    nums = [rng.randint(1, LIMIT) for _ in range(N)]
    window = N // 3
    return {"nums": nums, "k": (LIMIT // 2) * window * window}
