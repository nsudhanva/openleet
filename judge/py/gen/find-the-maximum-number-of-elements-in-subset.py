"""Maximum Subset of the pattern [x, x^2, x^4, ..., x^2, x] at n = 10^5: many 1s plus square
chains (with paired copies) up to 10^9, mixed with random noise."""

SEEDS = 3
N = 10**5


def generate(rng):
    nums = [1] * rng.choice([0, 7, 30000, 30001])
    while len(nums) < N * 3 // 4:
        x = rng.randint(2, 31622)
        while x <= 10**9 and len(nums) < N * 3 // 4:
            nums.extend([x] * rng.choice([1, 2, 2, 3]))
            x *= x
    while len(nums) < N:
        nums.append(rng.randint(1, 10**9))
    nums = nums[:N]
    rng.shuffle(nums)
    return {"nums": nums}
