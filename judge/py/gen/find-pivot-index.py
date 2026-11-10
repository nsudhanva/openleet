"""Find Pivot Index at n = 10^4: a pivot built in late (or at the last index), or none at all."""

SEEDS = 3
N = 10**4


def generate(rng):
    nums = [rng.randint(-1000, 1000) for _ in range(N)]
    mode = 2 if rng.random() < 0.2 else rng.randrange(2)
    if mode == 2:
        return {"nums": nums}
    p = N - 1 if mode == 0 else rng.randrange(N * 3 // 4, N - 1)
    # Nudge the left side, within [-1000, 1000], until it sums to the right side.
    need = sum(nums[p + 1 :]) - sum(nums[:p])
    for i in range(p):
        if need == 0:
            break
        if need > 0:
            step = min(1000 - nums[i], need)
            nums[i] += step
            need -= step
        else:
            step = min(nums[i] + 1000, -need)
            nums[i] -= step
            need += step
    return {"nums": nums}
