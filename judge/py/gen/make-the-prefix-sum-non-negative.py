"""Make the Prefix Sum Non-negative at n = 7 * 10^4: 2 * 10^4 small negatives stay in the pool while
2.5 * 10^4 large ones each force a move, so finding the smallest by a scan is ~10^9 steps.
Large positives at the end keep the total >= 0."""

SEEDS = 2
SMALL = 2 * 10**4
BIG = 25 * 10**3
TOP = 10**9


def generate(rng):
    body = [-rng.randint(1, 1000) for _ in range(SMALL)]
    body += [-rng.randint(TOP // 2, TOP) for _ in range(BIG)]
    rng.shuffle(body)
    nums = [TOP, *body]
    need = -sum(nums)
    while need > 0:
        nums.append(min(TOP, need))
        need -= nums[-1]
    return {"nums": nums}
