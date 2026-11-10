"""Maximum Product Subarray at n = 2 * 10^4: long runs of +-1 with a few larger factors
(every subarray product stays within 2^30), split by zeros in one seed and unbroken in the
other, so quadratic scans do ~2 * 10^8 steps."""

SEEDS = 3
N = 2 * 10**4
BUDGET = 2**30


def segment(rng, length):
    values = [rng.choice((1, -1)) for _ in range(length)]
    product = 1
    for _ in range(rng.randint(0, 30)):
        v = rng.randint(2, 10)
        if product * v > BUDGET:
            break
        product *= v
        values[rng.randrange(length)] = v * rng.choice((1, -1))
    return values


def generate(rng):
    if rng.random() < 0.5:
        return {"nums": segment(rng, N)}
    nums = []
    while len(nums) < N:
        length = min(rng.randint(1, 3000), N - len(nums))
        nums.extend(segment(rng, length))
        if len(nums) < N:
            nums.append(0)
    return {"nums": nums}
