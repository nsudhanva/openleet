"""Product Except Self at n = 10^5: mostly +-1 with a few larger factors kept under 2^31, and
optionally one zero, so division-based and quadratic approaches both get tested."""

SEEDS = 2
N = 10**5


def generate(rng):
    nums = [rng.choice([1, -1]) for _ in range(N)]
    product = 1
    for _ in range(200):
        v = rng.randint(2, 30)
        if product * v > 2**31 - 1:
            break
        product *= v
        nums[rng.randrange(N)] = v * rng.choice([1, -1])
    if rng.random() < 0.5:
        i = rng.randrange(N)
        while abs(nums[i]) != 1:
            i = rng.randrange(N)
        nums[i] = 0
    return {"nums": nums}
