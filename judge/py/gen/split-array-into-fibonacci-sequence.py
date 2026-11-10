"""Split Array into Fibonacci at up to 200 digits: a real Fibonacci-like chain running up to the
32-bit limit, the same with one digit changed, or a long run of a repeated digit."""

from _shapes import pick_shape

SEEDS = 3


def generate(rng):
    shape = pick_shape(rng)
    if shape == 2:
        return {"num": rng.choice("019") * 200}
    a, b = rng.randint(0, 999), rng.randint(0, 999)
    parts = [str(a), str(b)]
    while True:
        a, b = b, a + b
        if b > 2**31 - 1 or sum(map(len, parts)) + len(str(b)) > 200:
            break
        parts.append(str(b))
    num = list("".join(parts))
    if shape == 1:
        i = rng.randrange(len(num) // 2, len(num))
        num[i] = str((int(num[i]) + rng.randint(1, 9)) % 10)
    return {"num": "".join(num)}
