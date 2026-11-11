"""Minimum Deletions to Make Array Divisible with 2 * 10^4 nums and 8 * 10^4 numsDivide, where each
failing candidate fails only on the last numsDivide value: 1106 distinct candidates against one
repeated value, or two candidates against all-distinct values, or 60 against 8 * 10^4 with no
answer."""

from _shapes import pick_shape

SEEDS = 3
N = 2 * 10**4
M = 8 * 10**4
X = 735134400  # 2^6 * 3^3 * 5^2 * 7 * 11 * 13 * 17, 1344 divisors
Y = 10080  # 2^5 * 3^2 * 5 * 7, 72 divisors, 99206 multiples up to 10^9
SPOIL = 4 * 2**20 - 1  # 3 * 1398101, odd, its low 20 bits all set: last in set order


def divisors(x):
    small = [d for d in range(1, int(x**0.5) + 1) if x % d == 0]
    return sorted({*small, *(x // d for d in small)})


def generate(rng):
    shape = pick_shape(rng)
    if shape == 0:
        # Even divisors of X divide every X but not the odd g = X / 64, and the ones below g
        # sort first, so each one is checked against all of numsDivide.
        g = X // 64
        fail = [d for d in divisors(X) if d % 2 == 0 and d < g][: N - 5]
        nums = fail + [rng.choice(fail) for _ in range(N - 5 - len(fail))] + [g] * 5
        rng.shuffle(nums)
        return {"nums": nums, "numsDivide": [X] * (M - 1) + [g]}
    if shape == 1:
        # The 2s divide every distinct multiple of 6 but not the odd SPOIL; the answer is the 3.
        nums = [2] * (N - 1) + [3]
        rng.shuffle(nums)
        div = [6 * v for v in rng.sample(range(1, 10**9 // 6), M - 1)]
        return {"nums": nums, "numsDivide": [*div, SPOIL]}
    # Every even divisor of Y divides every distinct multiple of Y but not the odd SPOIL, and
    # gcd(Y, SPOIL) = 3, so no deletion works and the answer is -1.
    fail = [d for d in divisors(Y) if d % 2 == 0]
    nums = fail + [rng.choice(fail) for _ in range(N - len(fail))]
    rng.shuffle(nums)
    div = [Y * v for v in rng.sample(range(1, 10**9 // Y + 1), M - 1)]
    return {"nums": nums, "numsDivide": [*div, SPOIL]}
