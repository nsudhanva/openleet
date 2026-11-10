"""Swap Adjacent in LR String at length 10^4: reachable results built by real moves (every L
pushed far left, or many random moves) and a perturbed, likely unreachable, result."""

from _shapes import pick_shape

SEEDS = 3
N = 10**4


def generate(rng):
    shape = pick_shape(rng)
    p = rng.uniform(0.1, 0.5)
    start = [rng.choice("LR") if rng.random() < p else "X" for _ in range(N)]
    if shape == 0:
        # Push every L as far left as it can go; R's stay put. Always reachable.
        result = ["X"] * N
        prev = -1
        for i, ch in enumerate(start):
            if ch == "L":
                prev += 1
                result[prev] = "L"
            elif ch == "R":
                prev = i
                result[i] = "R"
    else:
        result = start[:]
        for _ in range(3 * 10**5):
            i = rng.randrange(N - 1)
            pair = result[i] + result[i + 1]
            if pair in ("XL", "RX"):
                result[i], result[i + 1] = result[i + 1], result[i]
        if shape == 2:
            i = rng.randrange(N)
            result[i] = rng.choice([c for c in "LRX" if c != result[i]])
    return {"start": "".join(start), "result": "".join(result)}
