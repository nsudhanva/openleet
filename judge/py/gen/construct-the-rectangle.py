"""Construct the Rectangle with area near 10^7: a large prime (the search must walk all the
way down to width 1) or a highly composite area."""

SEEDS = 2


def is_prime(x):
    if x < 2:
        return False
    i = 2
    while i * i <= x:
        if x % i == 0:
            return False
        i += 1
    return True


def generate(rng):
    if rng.random() < 0.5:
        area = rng.randint(9 * 10**6, 10**7)
        while not is_prime(area):
            area -= 1
    else:
        area = rng.choice([9699690, 8648640, 7207200, 10**7])
    return {"area": area}
