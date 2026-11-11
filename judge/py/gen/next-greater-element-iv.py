"""Next Greater Element IV at n = 2 * 10^4 non-increasing values (with runs of equal values and
20 random ones at the end), so most answers are -1 and a scan to the right for each index is
~2 * 10^8 steps."""

SEEDS = 2
N = 2 * 10**4
TAIL = 20


def generate(rng):
    nums = sorted((rng.randint(0, 10**9) for _ in range(N - TAIL)), reverse=True)
    for i in range(0, N - TAIL - 10, 50):
        nums[i + 1 : i + 10] = [nums[i]] * 9
    nums += [rng.randint(0, 10**9) for _ in range(TAIL)]
    return {"nums": nums}
