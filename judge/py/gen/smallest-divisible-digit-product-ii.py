"""Smallest Divisible Digit Product II with a 2 * 10^5-digit num (zeros, digit runs) and t up
to 10^14 made of 2, 3, 5, 7 (solvable) or with a larger prime factor (answer -1)."""

SEEDS = 3
N = 2 * 10**5


def generate(rng):
    shape = rng.getrandbits(6) % 3
    if shape == 0:
        # A zero early forces the suffix to be rebuilt.
        digits = [rng.choice("123456789")] + [rng.choice("0123456789") for _ in range(N - 1)]
        digits[rng.randint(1, 10)] = "0"
    elif shape == 1:
        digits = ["9"] * N
    else:
        digits = [rng.choice("123456789")] + [rng.choice("1111123") for _ in range(N - 1)]
    if rng.random() < 0.8:
        t = 1
        while True:
            p = rng.choice([2, 3, 5, 7])
            if t * p > 10**14:
                break
            t *= p
    else:
        t = rng.choice([11, 13, 2 * 3 * 11, 10**14 - 1])
    return {"num": "".join(digits), "t": t}
