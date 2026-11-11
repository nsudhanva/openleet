"""Maximum Number of Non-Overlapping Subarrays With Sum Equals Target with 2 * 10^4 values, a
large target and the matching subarrays planted at the end, so trying every start for each end
is quadratic."""

SEEDS = 2
N = 2 * 10**4
PLANTED = 3
PART = 60


def generate(rng):
    target = rng.randint(3 * 10**5, 55 * 10**4)
    nums = [rng.randint(-(10**4), 10**4) for _ in range(N - PLANTED * PART)]
    for _ in range(PLANTED):
        # PART values near target / PART that sum to exactly target.
        part = [target // PART] * PART
        for i in range(target % PART):
            part[i] += 1
        for i in range(0, PART, 2):
            d = rng.randint(0, 500)
            part[i] += d
            part[i + 1] -= d
        nums += part
    return {"nums": nums, "target": target}
