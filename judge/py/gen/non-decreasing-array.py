"""Non-decreasing Array at n = 10^4: a sorted array with one spike, one dip or two separate
dips in its last 200 slots, so trying each index and rescanning is ~10^8 steps."""

from _shapes import pick_shape

SEEDS = 3
N = 10**4
TAIL = 200
TOP = 10**5


def generate(rng):
    shape = pick_shape(rng)
    # Kept one inside the bounds, so a spike or a dip always has room.
    nums = sorted(rng.randint(-TOP + 1, TOP - 1) for _ in range(N))
    if shape == 0:
        i = rng.randint(N - TAIL, N - 2)
        nums[i] = rng.randint(nums[i + 1] + 1, TOP)
    else:
        spots = [rng.randint(N - TAIL, N - 1)]
        if shape == 2:
            spots.append(rng.randint(N - TAIL, N - 1))
            while abs(spots[1] - spots[0]) < 3:
                spots[1] = rng.randint(N - TAIL, N - 1)
        for i in spots:
            nums[i] = rng.randint(-TOP, nums[i - 1] - 1)
    return {"nums": nums}
