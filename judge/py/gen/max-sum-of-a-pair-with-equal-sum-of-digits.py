"""Max Sum of a Pair With Equal Sum of Digits at n = 2 * 10^4 nine-digit values that all share one
digit sum, so one bucket holds every value and trying every pair, or every pair within a bucket,
is 2 * 10^8 checks."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    target = rng.randint(38, 45)
    nums = []
    while len(nums) < N:
        head = rng.randrange(10**7, 10**8)
        last = target - sum(map(int, str(head)))
        if 0 <= last <= 9:
            nums.append(head * 10 + last)
    return {"nums": nums}
