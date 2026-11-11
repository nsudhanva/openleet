"""Minimum Cost Homecoming of a Robot in a Grid on a 10^4 x 10^4 grid from one corner to the
other, so a shortest-path search or DP over the cells visits 10^8 of them."""

SEEDS = 2
SIDE = 10**4
LIMIT = 10**4


def generate(rng):
    rows = [rng.randint(0, LIMIT) for _ in range(SIDE)]
    cols = [rng.randint(0, LIMIT) for _ in range(SIDE)]
    if rng.random() < 0.5:
        start, home = [0, 0], [SIDE - 1, SIDE - 1]
    else:
        start, home = [SIDE - 1, 0], [0, SIDE - 1]
    return {"startPos": start, "homePos": home, "rowCosts": rows, "colCosts": cols}
