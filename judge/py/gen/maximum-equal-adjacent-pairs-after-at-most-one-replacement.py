"""Maximum Equal Adjacent Pairs After at Most One Replacement at n = 2 * 10^4: either one value at
every other index between random others, or a pool of a few thousand values with some equal
runs, so replacing and recounting for each position is ~4 * 10^8 steps."""

from _shapes import pick_shape

SEEDS = 2
N = 2 * 10**4
LIMIT = 10**9


def generate(rng):
    if pick_shape(rng) == 0:
        hub = rng.randint(1, LIMIT)
        return {"nums": [hub if i % 2 == 0 else rng.randint(1, LIMIT) for i in range(N)]}
    pool = rng.sample(range(1, LIMIT + 1), N // 8)
    nums = [rng.choice(pool)]
    for _ in range(N - 1):
        nums.append(nums[-1] if rng.random() < 0.1 else rng.choice(pool))
    return {"nums": nums}
