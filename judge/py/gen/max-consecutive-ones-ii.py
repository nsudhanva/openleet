"""Max Consecutive Ones II at n = 10^5 with 300, 10^4 or 2 * 10^4 zeros at random, so extending from
every start (long gaps) or flipping each zero and rescanning (many zeros) is >= 3 * 10^7 steps."""

from _shapes import pick_shape

SEEDS = 3
N = 10**5
ZEROS = (300, 10**4, 2 * 10**4)


def generate(rng):
    nums = [1] * N
    for i in rng.sample(range(N), ZEROS[pick_shape(rng)]):
        nums[i] = 0
    return {"nums": nums}
