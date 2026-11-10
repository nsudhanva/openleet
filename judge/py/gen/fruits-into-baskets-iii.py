"""Fruits Into Baskets III at n = 10^5: baskets ascending so each fruit's leftmost fit lies far to
the right, punishing the quadratic scan."""

SEEDS = 3
N = 10**5


def generate(rng):
    shape = rng.randrange(3)
    baskets = [rng.randint(1, 10**9) for _ in range(N)]
    if shape == 0:
        baskets.sort()
        fruits = sorted((rng.randint(1, 10**9) for _ in range(N)), reverse=True)
    elif shape == 1:
        baskets.sort()
        fruits = [rng.randint(1, 10**9) for _ in range(N)]
    else:
        fruits = [rng.randint(1, 10**9) for _ in range(N)]
    return {"fruits": fruits, "baskets": baskets}
