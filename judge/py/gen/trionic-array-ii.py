"""Trionic Array II at n = 3 * 10^4: one array-long rise, fall and rise with a few short trionic
bumps, so extending every start to the end is ~4 * 10^8 steps."""

SEEDS = 2
N = 3 * 10**4


def generate(rng):
    a, b = sorted(rng.sample(range(2, N - 2), 2))
    nums = [-(10**8)]
    for i in range(1, N):
        step = rng.randint(1, 10**4)
        nums.append(nums[-1] + (step if i < a or i > b else -step))
    for _ in range(rng.randint(3, 10)):
        i = rng.randrange(1, N - 1)
        nums[i] = rng.randint(-(10**9), 10**9)
    return {"nums": nums}
