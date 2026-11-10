"""Maximize Sum of Squares of Digits with num up to 2 * 10^5 digits and sum up to 2 * 10^6,
both feasible and infeasible (sum above 9 * num) cases."""

SEEDS = 3
NUM = 2 * 10**5


def generate(rng):
    num = rng.choice([NUM, rng.randint(10**5, NUM)])
    shape = rng.choice(["feasible", "tight", "infeasible"])
    if shape == "feasible":
        total = rng.randint(1, 9 * num)
    elif shape == "tight":
        total = 9 * num - rng.randint(0, 5)
    else:
        total = min(2 * 10**6, 9 * num + rng.randint(1, 1000))
    return {"num": num, "sum": total}
