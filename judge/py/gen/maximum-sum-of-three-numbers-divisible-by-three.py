"""Maximum Sum of Three Numbers Divisible by Three at n = 2 * 10^4: one 99999, a long block of
values = 1 (mod 3) in [60004, 70000], a single value = 2 (mod 3) and small noise, so a sorted
triple loop with branch-and-bound still scans the block for every pair, ~2 * 10^8 steps."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    block = [3 * rng.randint(20001, 23333) + 1 for _ in range(N - 2 - N // 10)]
    noise = [rng.randint(1, 30000) for _ in range(N // 10)]
    nums = [99999, 3 * rng.randint(15001, 16000) + 2, *block, *noise]
    rng.shuffle(nums)
    return {"nums": nums}
