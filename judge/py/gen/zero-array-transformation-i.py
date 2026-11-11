"""Zero Array Transformation I at 2 * 10^4 numbers and 2 * 10^4 queries spanning most of the
array, each number at most its coverage (true), so applying every query is ~3 * 10^8 steps."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    queries = []
    for _ in range(N):
        left = rng.randrange(N // 10)
        queries.append([left, rng.randrange(N - N // 10, N)])
    diff = [0] * (N + 1)
    for left, right in queries:
        diff[left] += 1
        diff[right + 1] -= 1
    nums, run = [], 0
    for i in range(N):
        run += diff[i]
        nums.append(rng.randint(max(0, run - 50), min(run, 10**5)))
    return {"nums": nums, "queries": queries}
