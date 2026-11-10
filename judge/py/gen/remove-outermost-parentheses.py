"""Remove Outermost Parentheses at length 10^5: one deeply nested primitive, or many small
primitives."""

SEEDS = 2
N = 10**5


def generate(rng):
    if rng.random() < 0.5:
        depth = N // 2
        return {"s": "(" * depth + ")" * depth}
    out, total = [], 0
    while total < N:
        size = min(rng.randint(1, 20), (N - total) // 2)
        bal, prim = 0, []
        opens = closes = 0
        while opens < size or closes < size:
            if opens < size and (bal == 0 or rng.random() < 0.5):
                prim.append("(")
                opens += 1
                bal += 1
            else:
                prim.append(")")
                closes += 1
                bal -= 1
        out.append("".join(prim))
        total += 2 * size
    return {"s": "".join(out)}
