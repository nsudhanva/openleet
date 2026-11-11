"""Adjacent Increasing Subarrays II at n = 2 * 10^4: short random runs with one increasing run
of about n / 2 at the end, so the answer is near n / 4 and trying each k with a linear check
does ~n / 4 full scans whether k counts up or down."""

SEEDS = 2
N = 2 * 10**4
LIMIT = 10**9


def generate(rng):
    run = N // 2 + rng.randint(-N // 200, N // 200)
    nums = [rng.randint(-LIMIT, LIMIT) for _ in range(N - run)]
    start = rng.randint(-LIMIT, LIMIT - 10 * run)
    nums += sorted(rng.sample(range(start, start + 10 * run), run))
    return {"nums": nums}
