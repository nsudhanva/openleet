"""Sum of Digit Differences of All Pairs at n = 2 * 10^4 nine-digit numbers, so comparing every
pair digit by digit is ~2 * 10^8 pair visits."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    digits = rng.choice(("0123456789", "1279"))
    nums = []
    for _ in range(N):
        nums.append(int(rng.choice("123456789") + "".join(rng.choice(digits) for _ in range(8))))
    return {"nums": nums}
