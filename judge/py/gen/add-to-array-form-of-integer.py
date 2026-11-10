"""Add to Array-Form at length 10^4: all nines plus k = 9999 carries through the whole array;
random digits otherwise."""

SEEDS = 2


def generate(rng):
    if rng.random() < 0.5:
        return {"num": [9] * 10**4, "k": 10**4 - 1}
    num = [rng.randint(1, 9)] + [rng.randint(0, 9) for _ in range(10**4 - 1)]
    return {"num": num, "k": rng.randint(1, 10**4)}
