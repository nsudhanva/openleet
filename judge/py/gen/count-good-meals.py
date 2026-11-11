"""Count Good Meals at n = 2 * 10^4 with mostly distinct values, half of them 2^p - x for an earlier
x, so many pairs qualify and testing every pair, of elements or of distinct values, costs ~10^8
steps."""

SEEDS = 2
N = 2 * 10**4
TOP = 2**20


def generate(rng):
    nums = [rng.randint(0, TOP)]
    while len(nums) < N:
        if rng.random() < 0.5:
            x = rng.choice(nums)
            nums.append((1 << rng.randint(min(x.bit_length(), 20), 20)) - x)
        else:
            nums.append(rng.randint(0, TOP))
    return {"deliciousness": nums}
