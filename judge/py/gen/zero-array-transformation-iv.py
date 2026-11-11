"""Zero Array Transformation IV at 10 numbers and 1000 short queries, the last number covered
only by the last query, so the answer is 1000 and redoing the subset sums from scratch for each
k is ~10^9 steps."""

SEEDS = 2
N = 10
Q = 1000


def generate(rng):
    queries = []
    for _ in range(Q - 1):
        left = rng.randrange(N - 1)
        queries.append([left, min(N - 2, left + rng.randint(0, 2)), rng.randint(1, 10)])
    last = rng.randint(1, 10)
    queries.append([N - 1, N - 1, last])
    # Each other number is a subset sum of the queries covering it in the first half.
    nums = [0] * N
    for left, right, val in queries[: Q // 2]:
        for i in range(left, right + 1):
            if nums[i] + val <= 1000 and rng.random() < 0.5:
                nums[i] += val
    nums[N - 1] = last
    return {"nums": nums, "queries": queries}
