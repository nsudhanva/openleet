"""Sign of the Product on 1000 values in [-100, 100] (the product overflows any fixed-width
integer), with or without a zero."""

SEEDS = 3


def generate(rng):
    shape = rng.getrandbits(6) % 3
    nums = [rng.choice([-100, -99, 100, 99, rng.randint(-100, 100)]) for _ in range(1000)]
    if shape < 2:
        nums = [x if x else 1 for x in nums]
        if shape == 1:
            nums[-1] = -nums[-1]
    else:
        nums[-1] = 0
    return {"nums": nums}
