"""Zero Array Transformation III at 2 * 10^4 numbers and 2 * 10^4 long queries, each number up
to half its coverage, so thousands of queries are live at once and picking the farthest-reaching
one by scanning (and dropping expired ones by rescanning) is ~10^8 steps."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    queries = []
    for _ in range(N):
        left = rng.randrange(N)
        queries.append([left, min(N - 1, left + rng.randint(N // 4, N // 2))])
    diff = [0] * (N + 1)
    for left, right in queries:
        diff[left] += 1
        diff[right + 1] -= 1
    nums, run = [], 0
    for i in range(N):
        run += diff[i]
        nums.append(rng.randint(0, run // 2))
    return {"nums": nums, "queries": queries}
