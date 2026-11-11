"""Steps to Make Array Non-decreasing at n = 3 * 10^4: a large first element before an
increasing run (n - 1 steps), or falling peaks each followed by a rising run, so simulating
the steps one round at a time is ~5 * 10^8 element visits."""

SEEDS = 2
N = 3 * 10**4
LIMIT = 10**9


def generate(rng):
    if rng.random() < 0.5:
        rest = sorted(rng.randint(1, LIMIT - 1) for _ in range(N - 1))
        return {"nums": [LIMIT, *rest]}
    nums, peak = [], LIMIT
    while len(nums) < N:
        run = min(N - len(nums) - 1, rng.choice((rng.randint(1, 50), rng.randint(N // 4, N // 2))))
        nums.append(peak)
        nums += sorted(rng.randint(1, peak - 1) for _ in range(run))
        peak -= rng.randint(1, 1000)
    return {"nums": nums}
