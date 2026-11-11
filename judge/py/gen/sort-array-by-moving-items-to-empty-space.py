"""Sort Array by Moving Items to Empty Space at n = 10^5. One seed is a random permutation, so
simulating the moves and searching for each item's position costs ~n^2 steps; the others are
products of 10^4 to 5 * 10^4 short cycles over shuffled positions, so rescanning from the start
for a misplaced item after each cycle costs ~10^9 steps."""

from _shapes import pick_shape

SEEDS = 3
N = 10**5


def generate(rng):
    nums = list(range(N))
    if pick_shape(rng) == 0:
        rng.shuffle(nums)
        return {"nums": nums}
    # Short cycles over random positions, handled left to right by an index-order rescan.
    cycle = rng.randint(2, 4)
    order = list(range(N))
    rng.shuffle(order)
    for start in range(0, N - cycle + 1, cycle):
        group = order[start : start + cycle]
        for a, b in zip(group, group[1:] + group[:1], strict=True):
            nums[a] = b
    return {"nums": nums}
