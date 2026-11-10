"""Solve the Equation at ~1000 characters with many x and constant terms on both sides: a unique
integer solution, infinite solutions, or no solution."""

SEEDS = 3


def term(coef, is_x, first):
    sign = "-" if coef < 0 else ("" if first else "+")
    mag = abs(coef)
    if is_x:
        return sign + ("x" if mag == 1 else f"{mag}x")
    return sign + str(mag)


def side(terms):
    return "".join(term(c, x, i == 0) for i, (c, x) in enumerate(terms))


def generate(rng):
    shape = rng.getrandbits(6) % 3
    left, length = [], 0
    while length < 300:
        c = rng.randint(1, 100) * rng.choice([1, -1])
        is_x = rng.random() < 0.5
        left.append((c, is_x))
        length += 5
    if shape == 1:
        right = list(left)
        rng.shuffle(right)
        return {"equation": side(left) + "=" + side(right)}
    if shape == 2:
        right = list(left)
        rng.shuffle(right)
        right.append((rng.randint(1, 100), False))
        return {"equation": side(left) + "=" + side(right)}
    right = []
    while length < 600:
        c = rng.randint(1, 100) * rng.choice([1, -1])
        right.append((c, rng.random() < 0.5))
        length += 5
    a = sum(c for c, x in left if x) - sum(c for c, x in right if x)
    if a == 0:
        left.append((1, True))
        a = 1
    c = sum(c for c, x in right if not x) - sum(c for c, x in left if not x)
    x0 = round(c / a) + rng.randint(-2, 2)
    delta = a * x0 - c
    while delta:
        step = max(-100, min(100, delta))
        right.append((step, False))
        delta -= step
    return {"equation": side(left) + "=" + side(right)}
