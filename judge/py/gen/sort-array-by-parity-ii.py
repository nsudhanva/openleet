"""Sort Array By Parity II at n = 2 * 10^4: exactly half even, in random order or with all odds
first."""

SEEDS = 2


def generate(rng):
    half = 10**4
    evens = [rng.randrange(0, 1001, 2) for _ in range(half)]
    odds = [rng.randrange(1, 1000, 2) for _ in range(half)]
    nums = odds + evens
    if rng.random() < 0.5:
        rng.shuffle(nums)
    return {"nums": nums}
