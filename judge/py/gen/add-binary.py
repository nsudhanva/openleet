"""Add Binary at length 10^4 each: all-ones operands carry through every digit, random ones
do not."""

SEEDS = 3


def generate(rng):
    shape = rng.choice(["ones", "random", "short"])
    if shape == "ones":
        return {"a": "1" * 10**4, "b": "1" * rng.randint(1, 10**4)}
    a = "1" + "".join(rng.choice("01") for _ in range(10**4 - 1))
    if shape == "short":
        return {"a": a, "b": rng.choice(["0", "1"])}
    b = "1" + "".join(rng.choice("01") for _ in range(rng.randint(0, 10**4 - 1)))
    return {"a": a, "b": b}
