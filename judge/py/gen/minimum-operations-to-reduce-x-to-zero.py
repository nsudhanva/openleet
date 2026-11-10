"""Minimum Operations to Reduce X to Zero at n = 10^5: x reachable from a long prefix plus
suffix, or x larger than the total (answer -1)."""

SEEDS = 3
N = 10**5


def generate(rng):
    nums = [rng.randint(1, 10**4) for _ in range(N)]
    total = sum(nums)
    kind = rng.choice(("reachable", "too-big", "random"))
    if kind == "reachable":
        a = rng.randint(0, N // 2)
        b = rng.randint(0, N // 2)
        x = sum(nums[:a]) + sum(nums[N - b :])
        x = max(1, x)
    elif kind == "too-big":
        x = min(10**9, total + 1)
    else:
        x = rng.randint(1, min(10**9, total))
    return {"nums": nums, "x": x}
