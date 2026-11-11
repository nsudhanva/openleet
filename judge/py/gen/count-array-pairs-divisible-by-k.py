"""Count Array Pairs Divisible by K at n = 2 * 10^4 with a highly composite k and each value a
random divisor of k times a random factor, so the gcds are varied and checking every pair costs
2 * 10^8 steps."""

SEEDS = 2
N = 2 * 10**4
LIMIT = 10**5
KS = (720, 5040, 10080, 55440)


def generate(rng):
    k = rng.choice(KS)
    divisors = [d for d in range(1, k + 1) if k % d == 0]
    nums = []
    for _ in range(N):
        d = rng.choice(divisors)
        nums.append(d * rng.randint(1, LIMIT // d))
    return {"nums": nums, "k": k}
